from concurrent import futures

import grpc
import kvs_pb2
import kvs_pb2_grpc

from time import time
from sys import argv

from mqtt import client, qos
from colors import BLUE, GREEN, RESET


class KeyValueStore(kvs_pb2_grpc.KeyValueStoreServicer): 

    keys = {}
    mqtt_msg = False

    def __init__(self):
        def on_message(client, userdata, data):
            self.mqtt_msg = True
            decoded_msg = data.payload.decode('utf-8')
            [key, value, version] = (decoded_msg[1:-1].split(", "))

            value = value if value else None
            version = int(version) if version else None

            if data.topic == "valkyrie/put":
                print(f"\n{GREEN}> Sync key \"{key}\" with value \"{value}\" (put){RESET}")
                self.Put(kvs_pb2.KeyValueRequest(key=key, val=value), context=None)
            elif data.topic == "valkyrie/del":
                print(f"\n{GREEN}> Sync key \"{key}\" (del){RESET}")
                self.Del(kvs_pb2.KeyRequest(key=key, ver=version), context=None)
            elif data.topic == "valkyrie/trim":
                print(f"\n{GREEN}> Sync key \"{key}\" (trim){RESET}")
                self.Trim(kvs_pb2.KeyRequest(key=key, ver=version), context=None)

        client.on_message = on_message
        # print("Construtor")

    def Get(self, request, context):
        if len(request.key) == 0:
            msg = "Length of key must be greater or equal to 1"
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return kvs_pb2.KeyValueVersionReply()
        
        findKey = self.keys.get(request.key)

        value, version = None, None

        if findKey != None:
            # print("there is key")
            if request.ver <= 0:
                (value, version) = findKey[-1]
            else:
                for i in range(len(findKey)-1,-1,-1):
                    if findKey[i][1] == request.ver or findKey[i][1] < request.ver:
                        (value, version) = findKey[i]
                        break

        print(f"\n{BLUE}Get key: {request.key} val: {value} ver: {version}{RESET}")
        return kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version or request.ver)
    
    def GetRange(self, request, context):
        print(f"\n{BLUE}Get range:{RESET}")
        greatest_version = request.fr.ver if request.fr.ver > request.to.ver else request.to.ver

        fr_version = None if request.fr.ver <= 0 else greatest_version
        fr = self.Get(kvs_pb2.KeyRequest(key=request.fr.key, ver=fr_version), context)

        to_version = None if request.to.ver <= 0 else greatest_version
        to = self.Get(kvs_pb2.KeyRequest(key=request.to.key, ver=to_version), context)

        for key in sorted(self.keys):
            found_data = self.Get(kvs_pb2.KeyRequest(key=key, ver=greatest_version), context=context)

            if fr.key <= key and key <= to.key and found_data.ver > 0:
                yield kvs_pb2.KeyValueVersionReply(key=key, val=found_data.val, ver=found_data.ver)
    
    def GetAll(self, request_iterator, context):
        print(f"\n{BLUE}Get all:{RESET}")
        requests = []
        responses = {}

        for request in request_iterator:
            requests.append(request)

        def getVersions(request):
            return request.ver
        
        greatest_version = max(list(map(getVersions, requests)))

        for request in requests:            
            version = None if request.ver <= 0 else greatest_version
            found_data = self.Get(kvs_pb2.KeyRequest(key=request.key, ver=version), context)
            responses[found_data.key] = found_data

        for key in sorted(responses.keys()):
            yield responses[key]
    
    def Put(self, request, context):
        if len(request.key) == 0:
            msg = "Length of key must be greater or equal to 1"
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return kvs_pb2.PutReply()
        
        if len(request.val) == 0:
            msg = "Value cannot be empty on a Put request"
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return kvs_pb2.PutReply()
        
        findKey = self.keys.get(request.key)

        if findKey == None:
            old_value, old_version = "", 0
            self.keys[request.key] = []
        else:
            (old_value, old_version) = findKey[-1]

        version = int(round(time() * 1000))
        self.keys[request.key].append((request.val, version))

        if self.mqtt_msg:
            self.mqtt_msg = False
        else:
            client.publish("valkyrie/put", f"({request.key}, {request.val}, {version})", qos)

        print(f"\n{BLUE}Put key: {request.key} val: {request.val} ver: {version}{RESET}")
        return kvs_pb2.PutReply(key=request.key, old_val=old_value, old_ver=old_version, ver=version)
    
    def PutAll(self, request_iterator, context):
        for request in request_iterator:

            response = self.Put(kvs_pb2.KeyValueRequest(key=request.key, val=request.val), context)
            
            yield response
    
    def Del(self, request, context):
        if len(request.key) == 0:
            msg = "Length of key must be greater or equal to 1"
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return kvs_pb2.KeyValueVersionReply()

        if request.key in self.keys:
            (value, version) = self.keys.pop(request.key)[-1]
        else:
            value, version = "", 0

        if self.mqtt_msg:
            self.mqtt_msg = False
        else:
            client.publish("valkyrie/del", f"({request.key}, 0, 0)", qos)

        print(f"\n{BLUE}Delete key: {request.key} val: {value} ver: {version}{RESET}")
        return kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version)
    
    def DelRange(self, request, context):
        print(f"\n{BLUE}Delete range:{RESET}")
        responses = []

        for key in self.keys:
            if request.fr.key <= key and key <= request.to.key:
                client.publish("valkyrie/del", f"({key}, 0, 0)", qos)
                responses.append(kvs_pb2.KeyRequest(key=key))

        for response in responses:
            yield self.Del(request=response, context=context)
    
    def DelAll(self, request_iterator, context):
        for request in request_iterator:
            
            response = self.Del(kvs_pb2.KeyRequest(key=request.key), context)

            yield response
    
    def Trim(self, request, context):
        
        if len(request.key) == 0:
            msg = "Length of key must be greater or equal to 1"
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return kvs_pb2.KeyValueVersionReply()

        findKey = self.keys.get(request.key)

        if findKey == None:
            value, version = "", 0
        else:
            (value, version) = findKey[-1]
            self.keys[request.key] = [findKey[-1]]

        if self.mqtt_msg:
            self.mqtt_msg = False
        else:
            client.publish("valkyrie/trim", f"({request.key}, 0, 0)", qos)

        print(f"\n{BLUE}Trim key: {request.key} val: {value} ver: {version}{RESET}")
        return kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version)

def serve():
    server_port = argv[1]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store = KeyValueStore()
    kvs_pb2_grpc.add_KeyValueStoreServicer_to_server(store, server)
    server.add_insecure_port("[::]:" + server_port)
    server.start()
    client.loop_start()
    print("Server started... Port: " + server_port)
    server.wait_for_termination()
    client.loop_stop()

if __name__ == "__main__":
    try:
        serve()
    except (KeyboardInterrupt):
        print("\nStopping server...")