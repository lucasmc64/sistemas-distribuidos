import grpc
import kvs_pb2
import kvs_pb2_grpc

from sys import argv

def put_keys():
    keys = [
        kvs_pb2.KeyValueRequest(key="chave1",val="wow"),
        kvs_pb2.KeyValueRequest(key="chave2",val="seila"),
        kvs_pb2.KeyValueRequest(key="chave3",val="pfFuncionaa")
    ]

    for k in keys:
        yield k

def run():
    with grpc.insecure_channel("localhost:" + argv[1]) as channel:
        stub = kvs_pb2_grpc.KeyValueStoreStub(channel)

        while True:
            print("--- Key Value Store ---")
            print("1. Get")
            print("2. GetRange (WIP)")
            print("3. GetAll (WIP)")
            print("4. Put")
            print("5. PutAll")
            print("6. Del")
            print("7. DelRange (WIP)")
            print("8. DellAll")
            print("9. Trim")
            print("10. Exit")

            op = int(input("Select operation: "))

            if op == 1:
                # get
                #response = stub.Get(kvs_pb2.KeyRequest(key="chave1"))
                key = input("Key: ")
                ver = input("Ver: ")
                if ver == "":
                    ver = None
                else:
                    ver = int(ver)
                response = stub.Get(kvs_pb2.KeyRequest(key=key, ver=ver))


            elif op == 2:
                # getrange
                response = 0

            elif op == 3:
                # getall
                response = 0

            elif op == 4:
                # put
                response = stub.Put(kvs_pb2.KeyValueRequest(key="chave1",val="eabeb"))
    
            elif op == 5:
                # putall
                response = []
                for r in stub.PutAll(put_keys()):
                    response.append(r)

            elif op == 6:
                # del
                response = 0

            elif op == 7:
                # delrange
                response = 0

            elif op == 8:
                # delall
                response = 0

            elif op == 9:
                # trim
                response = 0

            elif op == 10:
                # exit
                print("Exiting...")
                break

            else:
                print("Invalid operation!")
                continue
        
            print(f"\nResponse: {response}")


if __name__ == "__main__":
    run()
