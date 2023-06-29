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
from control import Control
import speech


mouth = speech.TTSpeech()
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
        if dictr != prevdictr:
            prevdictr = copy.deepcopy(dictr)
            if not dictr['running']:
                break
            if dictr["US_measure"] and not Control.sensor:
                Control.sensor = True
                sensors.start_thread()
            Control.sensor = dictr['US_measure']
            
            if dictr['buzzer'] == 'whole':
                bz.play_whole()
            #if dictr['parameter'] in :
            elif dictr["buzzer"] != "":
                bz.play(dictr["buzzer"])
            if dictr['say'] != '':
                mouth.say(dictr["say"])
            if dictr['dot'] != "":
                if dictr['dot'] == 'animation':
                    dotMatrix.animation()
                elif dictr["dot"] == 'clear':
                    dotMatrix.matrix_clear()
                else:
                    dotMatrix.show(dictr["dot"])
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
bz.__del__()
dotMatrix.__del__()
