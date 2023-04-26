import RPi.GPIO as GPIO
import time
import servo

srv = servo.Servo()

try:
    while True:
        for i in range(0,180):
            srv.servoPulse("horizontal", i)
        for i in range(0,180):
            srv.servoPulse("vertical", i)

        for i in range(0,180):
            i = 180 - i
            srv.servoPulse("horizontal", i)
        for i in range(0,180):
            i = 180 - i
            srv.servoPulse("vertical", i)

        for j in range(0, 50):
            srv.servoPulse("horizontal", 90)
        for j in range(0, 50):
            srv.servoPulse("vertical", 90)
        time.sleep(2)
except KeyboardInterrupt:
    pass
GPIO.cleanup()