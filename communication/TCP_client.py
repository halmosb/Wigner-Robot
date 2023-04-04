
import socket
import json
import copy

bufsize=1024
data = 'start'
prevdict = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.connect(('localhost', 8100))
    while True:
        data = tcp_socket.recv(1024).decode('utf-8')
        try:
            dict = json.loads(data)
            print(dict, prevdict==dict)
            prevdict = copy.deepcopy(dict)
            if dict['message'] == 'end':
                break
        except:
            break
print("Closing socket")
tcp_socket.close()
