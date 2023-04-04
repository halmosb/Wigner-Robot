import socket
import json
import keyboard
import numpy as np

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
server_address = ('192.168.137.1', 8100)
tcp_socket.bind(server_address)
# 
tcp_socket.listen(1)
print("Waiting for connection")
connection, client = tcp_socket.accept()
message = 'start'

speed = np.array([0,0])
kin = ''
while kin != 'q':
    kin = keyboard.read_key()
    if kin == 'up' :
        dv = [1,1]
    elif kin == 'down' :
        dv = [-1,-1]
    elif kin == 'right' :
        dv = [-1,1]
    elif kin == 'left' :
        dv = [-1,1]
    elif kin == 'q' :
        dv = [0,0]
    else:
        continue
    speed = np.array([ min( max(speed[i] + dv[i] ,0),100) for i in range(2) ])
    print(f'speed = {speed}')
    dict = {
        'message' : kin,
        'speed' : speed
    }
    try:
        connection.sendall(json.dumps(dict).encode('utf-8'))
    except:
        print('send failed')


connection.close()
tcp_socket.close()
