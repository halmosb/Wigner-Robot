import RPi.GPIO as GPIO
import time

class Servo:

    def __init__(self):
        self.us_servo=5
        self.camera_horizontal = 7
        self.camera_vertical = 6
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.names = {
            "us" : self.us_servo,
            "horizontal" : self.camera_horizontal,
            "vertical" : self.camera_vertical
        }
        self.repeat = {
            "us" : 5,
            "horizontal" : 5,
            "vertical" : 5
        }

        GPIO.setup(self.camera_horizontal, GPIO.OUT)
        GPIO.setup(self.us_servo, GPIO.OUT)
        GPIO.setup(self.camera_vertical, GPIO.OUT)
    
    def servoPulse(self, servoID, myangle):
        servoPin = self.names[servoID]
        pulsewidth = (myangle*11) + 500  # The pulse width
        irep = self.repeat[servoID]
        for i in range(irep) :
            GPIO.output(servoPin,GPIO.HIGH)
            time.sleep(pulsewidth/1000000.0)
            GPIO.output(servoPin,GPIO.LOW)
            #time.sleep(20.0/1000 - pulsewidth/1000000.0) # The cycle of 20 ms
            time.sleep(50.0/1000) # The cycle of 50 ms

    
    def __del__(self):
        GPIO.cleanup()
