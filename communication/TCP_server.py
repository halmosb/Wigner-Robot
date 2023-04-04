import socket
import json

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
server_address = ('localhost', 8100)
tcp_socket.bind(server_address)
 
tcp_socket.listen(1)
print("Waiting for connection")
connection, client = tcp_socket.accept()
message = 'start'

while message!= 'end':
    try:
        message = input('type message > ')
        dict = {
            'message' : message,
            'speed' : {
                "UL": 20,
                "LL": 20,
                "UR": 20,
                "LR": 20
            }
        }
        connection.sendall(json.dumps(dict).encode('utf-8'))
    except:
        print('send failed')

connection.close()
tcp_socket.close()
