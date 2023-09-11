from concurrent import futures

import grpc
import kvs_pb2
import kvs_pb2_grpc

from time import time
from sys import argv

keys = {}

class KeyValueStore(kvs_pb2_grpc.KeyValueStoreServicer):
    
    def Get(self, request, context):
        # do something
        return kvs_pb2.KeyValueVersionReply("","",0)
    
    def GetRange(self, request, context):
        # do something
        for key in keys:
            if True:
                yield kvs_pb2.KeyValueVersionReply()
    
    def GetAll(self, request_iterator, context):
        # do something
        for request in request_iterator:
            # something
            yield kvs_pb2.KeyValueVersionReply()
    
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
            yield kvs_pb2.KeyValueVersionReply()
    
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
            keys[request.key] = findKey[-1]

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