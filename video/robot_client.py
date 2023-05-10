import motor
import sensor
import socket
import json
import copy
from UDPwebcam import UDPwebcam_sender
import servo
import sensor
import buzzer

song =  [
    (330, 0.5),  # E4 for half a second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (330, 0.5),  # E4 for half a second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (330, 0.5),  # E4 for half a second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (330, 0.5),  # E4 for half a second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (330, 0.5),  # E4 for half a second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (440, 1),    # A4 for one second
    (440, 1),    # A4 for one second
    (440, 1),    # A4 for one second
    (415, 1),    # G#4 for one second
    (370, 1),    # F#4 for one second
    (330, 1),    # E4 for one second
    (440, 1),    # A4 for one second
    (440, 1),    # A4 for one second
    (440, 1),    # A4 for one second
    (415, 1),    # G#4 for one second
    (370, 1),    # F#4 for one second
    (330, 1),    # E4 for one second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (494, 1),    # B4 for one second
    (494, 1),    # B4 for one second
    (494, 1),    # B4 for one second
    (440, 1),    # A4 for one second
    (370, 1),    # F#4 for one second
    (330, 1),    # E4 for one second
    (494, 1),    # B4 for one second
    (494, 1),    # B4 for one second
    (494, 1),    # B4 for one second
    (440, 1),    # A4 for one second
    (370, 1),    # F#4 for one second
    (330, 1),    # E4 for one second
    (370, 0.5),  # F#4 for half a second
    (415, 0.5),  # G#4 for half a second
    (330, 1)     # E4 for one
]

masiksong = [
    (440, 0.5),  # A4 for half a second
    (494, 0.5),  # B4 for half a second
    (523, 1),    # C5 for one second
    (587, 1),    # D5 for one second
    (659, 1),    # E5 for one second
    (587, 2),    # D5 for two seconds
    (523, 2),    # C5 for two seconds
    (440, 2),    # A4 for two seconds
    (392, 2),    # G4 for two seconds
    (349, 2),    # F4 for two seconds
    (293, 4)     # D4 for four seconds
]

servMotors = servo.Servo()
ultar = sensor.Sensor()
bz = buzzer.Buzzer()

with open('settings.json') as f:
    settings = json.load(f)


motors = motor.Motor()
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
        if dictr['message'] == "violent":
            bz.play(song)
        if dictr['message'] == "nino":
            bz.play([[400,1],[262,1],[400,1],[262,1],[400,1],[262,1],[400,1],[262,1]])
        if dictr['message'] == "masiksong":
            bz.play(masiksong)
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
