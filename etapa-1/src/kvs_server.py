from concurrent import futures

import grpc
import kvs_pb2
import kvs_pb2_grpc

from time import time
from sys import argv

keys = {}

class KeyValueStore(kvs_pb2_grpc.KeyValueStoreServicer):
    
    def Get(self, request, context):
        findKey = keys.get(request.key)

        value, version = None, None

        if findKey != None:
            print("there is key")
            if request.ver <= 0:
                (value, version) = findKey[-1]
            else:
                for i in range(len(findKey)-1,-1,-1):
                    if findKey[i][1] == request.ver or findKey[i][1] < request.ver:
                        (value, version) = findKey[i]
                        break

        print(f"Get key: {request.key} val: {value} ver: {version}")
        return kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version or request.ver)
    
    def GetRange(self, request, context):
        greatest_version = request.fr.ver if request.fr.ver > request.to.ver else request.to.ver

        fr_version = None if request.fr.ver <= 0 else greatest_version
        fr = self.Get(kvs_pb2.KeyRequest(key=request.fr.key, ver=fr_version), context)

        to_version = None if request.to.ver <= 0 else greatest_version
        to = self.Get(kvs_pb2.KeyRequest(key=request.to.key, ver=to_version), context)

        for key in sorted(keys):
            found_data = self.Get(kvs_pb2.KeyRequest(key=key, ver=greatest_version), context=context)

            if fr.key <= key and key <= to.key and found_data.ver > 0:
                yield kvs_pb2.KeyValueVersionReply(key=key, val=found_data.val, ver=found_data.ver)
    
    def GetAll(self, request_iterator, context):
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
        findKey = keys.get(request.key)

        if findKey == None:
            old_value, old_version = "", 0
            keys[request.key] = []
        else:
            (old_value, old_version) = findKey[-1]

        version = int(round(time() * 1000))
        keys[request.key].append((request.val, version))
        print(f"new key/update: {request.key} {request.val} {version}")
        return kvs_pb2.PutReply(key=request.key, old_val=old_value, old_ver=old_version, ver=version)
    
    def PutAll(self, request_iterator, context):
        
        for request in request_iterator:

            print("on a request")
            findKey = keys.get(request.key)

            if findKey == None:
                old_value, old_version = "", 0
                keys[request.key] = []
            else:
                (old_value, old_version) = findKey[-1]

            version = int(round(time() * 1000))
            keys[request.key].append((request.val, version))
            print(f"new key/update: {request.key} {request.val} {version}")
            
            yield kvs_pb2.PutReply(key=request.key, old_val=old_value, old_ver=old_version, ver=version)
    
    def Del(self, request, context):
        if request.key in keys:
            (value, version) = keys.pop(request.key)[-1]
        else:
            value, version = "", 0

        return kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version)
    
    def DelRange(self, request, context):
        # do something
        for key in keys:
            # something
            yield kvs_pb2.KeyValueVersionReply(key="", val="", ver=0)
    
    def DelAll(self, request_iterator, context):
        
        for request in request_iterator:
            if request.key in keys:
                (value, version) = keys.pop(request.key)[-1]
            else:
                value, version = "", 0
            
            yield kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version)
    
    def Trim(self, request, context):
        findKey = keys.get(request.key)

        if findKey == None:
            value, version = "", 0
        else:
            (value, version) = findKey[-1]
            keys[request.key] = [findKey[-1]]

        return kvs_pb2.KeyValueVersionReply(key=request.key, val=value, ver=version)
    
def serve():
    port = argv[1]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvs_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStore(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started... Port: " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()