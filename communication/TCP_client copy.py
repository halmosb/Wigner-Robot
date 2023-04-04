import socket

tcp_socket = socket.create_connection(('localhost', 8100))
 
try:
    data = str.encode('alma')
    tcp_socket.sendall(data)
finally:
    print("Closing socket")
    tcp_socket.close()
