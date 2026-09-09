## for testing how does the client receive data sent by the server
import socket
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5000))
data= client_socket.recv(1024)
print(data.decode())

