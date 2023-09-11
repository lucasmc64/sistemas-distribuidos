import grpc
import kvs_pb2
import kvs_pb2_grpc

from sys import argv

def run():
    with grpc.insecure_channel("localhost:" + argv[1]) as channel:
        stub = kvs_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Put(kvs_pb2.KeyValueRequest(key="chave1",val="eabeb"))
    print("Received put reply:")
    print("Key: "+response.key)
    print("Old value: "+response.old_val)
    print("Old version: "+str(response.old_ver))
    print("Current version: "+str(response.ver))

if __name__ == "__main__":
    run()
