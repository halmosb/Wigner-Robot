import motor
import socket
import json
import copy
from UDPwebcam import UDPwebcam_sender

with open('settings.json') as f:
    settings = json.load(f)

"""class Motor():
    def __init__(self, settings):
        print(f'my settings: {settings}')
    def set_speed(self, speed) :
        print(speed)
"""
motors = motor.Motor()
#motors = Motor(settings=settings)
prevspeed=[]


sender = UDPwebcam_sender(bufsize= settings['bufsize'], IP= settings['IP'], port=settings['webcam_port'])
sender.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.connect((settings['IP'], settings['control_port']))
    while True:
        data = tcp_socket.recv(1024).decode('utf-8')
        if len(data) == 0:
            break
        if len(data) > 45:
            print('{'+data.split('}{')[-1])
            continue
        dict = json.loads(data)
        print(dict)
        prevdict = copy.deepcopy(dict)
        if dict['message'] == 'q':
            break
        speed = dict['speed']
        if speed != prevspeed:
            prevspeed = speed
            motors.set_speed(speed)
#print("Closing socket")
tcp_socket.close()
sender.stop()
