import sys
import socket

HOST = sys.argv[1]
start_port= int(sys.argv[2])
end_port= int(sys.argv[3])
def check_port(HOST, PORT): 
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"Port {PORT}: OPEN")
    except ConnectionRefusedError:
        print(f"Port {PORT}: CLOSED")
    client_socket.close()
if(start_port<0 or end_port<0 or start_port> end_port ):
    print("Provide valid start and end port")
    sys.exit()
for i in range(start_port, end_port+1):
    check_port(HOST, i)
    


