import motor
import sensor
import socket
import json
import copy
from UDPwebcam import UDPwebcam_sender
import servo
import sensor
import buzzer
import dot_matrix



servMotors = servo.Servo()
ultar = sensor.Sensor()
bz = buzzer.Buzzer()
dotMatrix = dot_matrix.DotMatrix()

with open('settings.json') as f:
    settings = json.load(f)


motors = motor.Motor(frequency=settings["maxSpeed"])
sensors = sensor.Sensor()
#motors = Motor(settings=settings)
prevspeed = []
prevangles = [90,90,90]


sender = UDPwebcam_sender(bufsize= settings['bufsize'], IP= settings['IP'], port=settings['webcam_port'])
sender.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.connect((settings['IP'], settings['control_port']))
    while True:
        data = tcp_socket.recv(1024).decode('utf-8')
        if len(data) == 0:
            break
        if len(data.split("}{")) > 1:
            print("Fixed data")
            data = '{'+data.split('}{')[-1]
        dictr = json.loads(data)
        print(dictr)
        prevdictr = copy.deepcopy(dictr)
        if dictr['message'] == 'q':
            break
        if dictr['message'] =='measure':
            sender.dist = sensors.distance()
        if dictr['message'] == 'buzzer':
            print("Got buzzer")
            if dictr['parameter'] == "violent":
                print("got violent")
                bz.play('mexican')
            if dictr['parameter'] == "nino":
                bz.play('nino')
            if dictr['parameter'] == "supermario":
                bz.play('supermario')
        if dictr['message'] == "dot":
            pass
        speed = dictr['speed']
        if speed != prevspeed:
            prevspeed = speed
            motors.set_speed(speed)
        angles = dictr["angles"]
        for i in range(3):
            if angles[i] != prevangles[i]:
                name = list(servMotors.names.keys())[i]
                servMotors.servoPulse(name,angles[i])
                prevangles[i] = angles[i]

#print("Closing socket")
tcp_socket.close()
sender.stop()
