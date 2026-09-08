import argparse
import sys
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
parser= argparse.ArgumentParser()
parser.add_argument("target")
parser.add_argument("--start", type=int)
parser.add_argument("--end", type=int)
parser.add_argument("--workers", type=int)
parser.add_argument("--timeout", type=float)
args= parser.parse_args()
target = args.target
start_port= args.start
timeout= args.timeout
end_port= args.end
if (
    start_port <= 0
    or end_port <= 0
    or start_port > end_port
    or start_port > 65535
    or end_port > 65535
    or timeout <= 0
    or args.workers <= 0
):
    print("Provide valid ports, timeout, and workers")
    sys.exit()
def resolve_target(target):
    start= time.perf_counter()
    
    try:
        ip= socket.gethostbyname(target)
        end= time.perf_counter()
        
        print(f"Resolved {target} -> {ip}")
        print(f"DNS resolution: {round(end- start, 3)} seconds")
        
        return ip
    except socket.gaierror:
        print(f"Could not resolve: {target}")
        sys.exit()
HOST = resolve_target(target)
def check_port(target, port,timeout): 
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.settimeout(timeout)
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



start = time.perf_counter()
with ThreadPoolExecutor(max_workers=args.workers) as executor:
    future_to_port= {}
    for i in range(start_port, end_port+1):
        future= executor.submit(check_port, HOST, i, timeout)
        future_to_port[future]= i
    for future in as_completed(future_to_port):
        port = future_to_port[future]
        result= future.result()
        print(f"Port {port}: {result}")
          
end= time.perf_counter()
print(f"Scan complete in {round(end-start, 3)} seconds")


