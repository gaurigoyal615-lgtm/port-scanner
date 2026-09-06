import argparse
import sys
import socket
import time
parser= argparse.ArgumentParser()
parser.add_argument("target")
parser.add_argument("--start", type=int)
parser.add_argument("--end", type=int)
args= parser.parse_args()
HOST = args.target
start_port= args.start
end_port= args.end
def check_port(target, port): 
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)
    try:
        client_socket.connect((target, port))
        return "OPEN"
    except ConnectionRefusedError:
        return "CLOSED"
    except TimeoutError:
        return "TIMEOUT"
    except ConnectionError as ce:
        return "ERROR"
    except OSError as e:
       return "ERROR"
    finally:
        client_socket.close()
if(start_port<=0 or end_port<=0 or start_port> end_port or  start_port>= 65536 or end_port>=65536 ):
    print("Provide valid start and end port")
    sys.exit()
start = time.perf_counter()
for i in range(start_port, end_port+1):
    result = check_port(HOST, i)
    if result== "OPEN":
        print(f"Port {i}: OPEN")
end= time.perf_counter()
print(f"Scan complete in {round(end-start, 3)} seconds")


