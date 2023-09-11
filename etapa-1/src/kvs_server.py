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
        checkKey = keys.get(request.key)

        if checkKey == None:
            old_value,old_version = "",0
        else:
            (old_value,old_version) = checkKey

        version = int(round(time()*1000))
        keys[request.key] = (request.val,version)
        print(f"new key/update: {request.key} {request.val} {version}")
        return kvs_pb2.PutReply(
                                key=request.key,
                                old_val=old_value,
                                old_ver=old_version,
                                ver=version
                                )
    
    def PutAll(self, request_iterator, context):
        # do something
        for request in request_iterator:
            # something
            yield kvs_pb2.PutReply()
    
    def Del(self, request, context):
        # do something
        return kvs_pb2.KeyValueVersionReply()
    
    def DelRange(self, request, context):
        # do something
        for key in keys:
            # something
            yield kvs_pb2.KeyValueVersionReply()
    
    def DelAll(self, request_iterator, context):
        # do something
        for request in request_iterator:
            # something
            yield kvs_pb2.KeyValueVersionReply()
    
    def Trim(self, request, context):
        # do something
        return kvs_pb2.KeyValueVersionReply()
    
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