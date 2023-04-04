import socket
import json
import keyboard
import numpy as np
import time

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
server_address = ('192.168.137.1', 8100)
tcp_socket.bind(server_address)
# 
tcp_socket.listen(1)
print("Waiting for connection")
connection, client = tcp_socket.accept()
print(f'connected to {client}')
message = 'start'

speed  = np.array([0,0], dtype=float)
kin = ' '
while kin != 'q':
    kin = keyboard.read_key()
    if kin == 'up' :
        dv = np.array([1,0], dtype=float)
    elif kin == 'down' :
        dv = np.array([-1,0], dtype=float)
    elif kin == 'right' :
        dv = np.array([0,1], dtype=float)
    elif kin == 'left' :
        dv = np.array([0,-1], dtype=float)
    elif kin == 'space' :
        dv = -speed
    elif kin == 'q' :
        dv = np.array([0,0], dtype=float)
    else:
        continue
    speed = np.array([ min( max(speed[i] + dv[i] ,-100.0),100.0) for i in range(2) ])
    print(f'speed = {speed}')
    dd = {
        'message' : kin,
        'speed' : list(speed)
    }
    connection.sendall(json.dumps(dd).encode('utf-8'))
    time.sleep(0.1)
#    except:
#        print('send failed')


connection.close()
tcp_socket.close()
 