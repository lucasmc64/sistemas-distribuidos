import grpc
import kvs_pb2
import kvs_pb2_grpc

from sys import argv
from colors import RED, BLUE, GREEN, YELLOW, LIGHT_CYAN, RESET, BOLD

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
    print(f"\n{YELLOW}> Enter an empty key to finish request!{RESET}")

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

def format_to_print(info):
    result = []
    
    for [descriptor, value] in info.ListFields():
        result.append(f"{LIGHT_CYAN}{descriptor.name}={RESET}{value}")
       
    return f"\n({', '.join(result)})"

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
            try:

                op = input("\nSelect operation: ")
                result = ""
                
                if op.isdigit():
                    op = int(op)

                if op == 1:
                    # get
                    
                    key = input("\nKey: ")
                    ver = input("Ver: ")

                    if ver == "":
                        ver = None
                    else:
                        ver = int(ver)

                    response = stub.Get(kvs_pb2.KeyRequest(key=key, ver=ver))
                    result = format_to_print(response)

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
                    
                    for response in stub.GetRange(kvs_pb2.KeyRange(fr=fr, to=to)):
                        result += format_to_print(response)

                elif op == 3:
                    # getall

                    for response in stub.GetAll(get_all_requests()):
                        result += format_to_print(response)

                elif op == 4:
                    # put

                    key = input("\nKey: ")
                    val = input("Val: ")
                    
                    response = stub.Put(kvs_pb2.KeyValueRequest(key=key,val=val))
                    result = format_to_print(response)
        
                elif op == 5:
                    # putall

                    keys = input("\nKeys: ").split()
                    vals = input("Vals: ").split()

                    if len(keys) != len(vals):
                        print(f"\n{RED}Missing key or value!{RESET}")
                        continue
                    
                    for response in stub.PutAll(put_requests(keys, vals)):
                        result += format_to_print(response)

                elif op == 6:
                    # del

                    key = input("\nKey: ")

                    response = stub.Del(kvs_pb2.KeyRequest(key=key))
                    result = format_to_print(response)

                elif op == 7:
                    # delrange

                    fr = {}
                    to = {}

                    fr["key"] = input("\nFrom key: ")
                    to["key"] = input("To key: ")
                    
                    for response in stub.DelRange(kvs_pb2.KeyRange(fr=fr, to=to)):
                        result += format_to_print(response)

                elif op == 8:
                    # delall

                    keys = input("\nKeys: ").split()
                    
                    for response in stub.DelAll(del_requests(keys)):
                        result += format_to_print(response)

                elif op == 9:
                    # trim

                    key = input("\nKey: ")
                    
                    response = stub.Trim(kvs_pb2.KeyRequest(key=key))
                    result = format_to_print(response)

                elif op == 10:
                    # exit
                    
                    print(f"\n{BLUE}> Exiting...{RESET}")
                    break

                else:
                    # string or operation out of range

                    print(f"\n{RED}> Invalid operation!{RESET}")
                    continue
            
                print(f"\n{GREEN}> Response:{RESET}\n{result}")

            except grpc.RpcError as e: 
                # Catches grpc errors like server unavailable or network issues

                print(f"\n{RED}{BOLD}Error:{RESET}")
                print(f"{RED}{BOLD}{e.details()}{RESET}")
                status_code = e.code()
                print(f"{RED}{BOLD}{status_code.name}{RESET}")
                print(f"{RED}{BOLD}{status_code.value}{RESET}")

            except (TypeError, ValueError) as e:
                # Catches a type error when calling a function with the wrong type of arguments
                # or a value error when reading a string for version of key
                print(f"\n{RED}{BOLD}Error: {e}{RESET}")

            except KeyboardInterrupt:
                # Catches a keyboard interruption like Ctrl+C
                print(f"\n{BLUE}> Exiting...{RESET}")
                break

            except:
                # Catches all other unexpected errors
                print(f"\n{RED}{BOLD}An error occurred.{RESET}")


if __name__ == "__main__":
    run()
