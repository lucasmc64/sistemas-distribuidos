import grpc
import kvs_pb2
import kvs_pb2_grpc

from sys import argv

def put_requests(keys, vals):
    requests = []

    for i in range(len(keys)):
        requests.append(kvs_pb2.KeyValueRequest(key=keys[i], val=vals[i]))

    for r in requests:
        yield r

def del_requests(keys):
    requests = []

    for i in range(len(keys)):
        requests.append(kvs_pb2.KeyRequest(key=keys[i]))

    for r in requests:
        yield r

def get_all_requests():
    print("\n> Enter an empty key to finish request!")

    while True:
        key = input("\nKey: ")

        if len(key) == 0:
            break

        version = input("Version: ")

        if(len(version) > 0):
            version = int(version)
        else:
            version = None

        yield kvs_pb2.KeyRequest(key=key, ver=version)

def run():
    with grpc.insecure_channel("localhost:" + argv[1]) as channel:
        stub = kvs_pb2_grpc.KeyValueStoreStub(channel)

        print("--- Key Value Store ---")
        print(" 1. Get")
        print(" 2. GetRange")
        print(" 3. GetAll")
        print(" 4. Put")
        print(" 5. PutAll")
        print(" 6. Del")
        print(" 7. DelRange")
        print(" 8. DellAll")
        print(" 9. Trim")
        print("10. Exit")

        while True:

            op = int(input("\nSelect operation: "))

            if op == 1:
                # get
                #response = stub.Get(kvs_pb2.KeyRequest(key="chave1"))
                key = input("\nKey: ")
                ver = input("Ver: ")
                if ver == "":
                    ver = None
                else:
                    ver = int(ver)
                response = stub.Get(kvs_pb2.KeyRequest(key=key, ver=ver))

            elif op == 2:
                # getrange
                fr = {}
                to = {}

                fr["key"] = input("\nFrom key: ")
                fr["ver"] = input("From ver: ")

                if(len(fr["ver"]) == 0):
                    fr.pop("ver")
                else:
                    fr["ver"] = int(fr["ver"])

                to["key"] = input("To key: ")
                to["ver"] = input("To ver: ")
                
                if(len(to["ver"]) == 0):
                    to.pop("ver")
                else:
                    to["ver"] = int(to["ver"])

                response = []
                
                for r in stub.GetRange(kvs_pb2.KeyRange(fr=fr, to=to)):
                    response.append(r)

            elif op == 3:
                # getall
                response = []

                for r in stub.GetAll(get_all_requests()):
                    response.append(r)

            elif op == 4:
                # put
                key = input("\nKey: ")
                val = input("Val: ")
                response = stub.Put(kvs_pb2.KeyValueRequest(key=key,val=val))
    
            elif op == 5:
                # putall
                keys = input("\nKeys: ").split()
                vals = input("Values: ").split()

                if len(keys) != len(vals):
                    print("\nMissing key or value!")
                    continue
                else:
                    response = []
                    for r in stub.PutAll(put_requests(keys, vals)):
                        response.append(r)

            elif op == 6:
                # del
                key = input("\nKey: ")
                response = stub.Del(kvs_pb2.KeyRequest(key=key))

            elif op == 7:
                fr = {}
                to = {}

                fr["key"] = input("\nFrom key: ")
                to["key"] = input("To key: ")

                response = []
                
                for r in stub.DelRange(kvs_pb2.KeyRange(fr=fr, to=to)):
                    response.append(r)

            elif op == 8:
                # delall
                keys = input("\nKeys: ").split()
                response = []
                for r in stub.DelAll(del_requests(keys)):
                    response.append(r)

            elif op == 9:
                # trim
                key = input("\nKey: ")
                response = stub.Trim(kvs_pb2.KeyRequest(key=key))

            elif op == 10:
                # exit
                print("\nExiting...")
                break

            else:
                print("Invalid operation!")
                continue
        
            print(f"\nResponse: {response}")


if __name__ == "__main__":
    run()
