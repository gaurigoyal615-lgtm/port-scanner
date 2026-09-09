import socket
HOST= "127.0.0.1"
PORT= 5000
server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

connection, address= server_socket.accept()
connection.send(b"HELLO FROM THE TEST SERVER ")
print(f"Connection received from {address}")

connection.close()
server_socket.close()



