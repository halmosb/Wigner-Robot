import RPi.GPIO as GPIO
import time
 


class Sensor:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.US_TRIGGER = 9
        self.US_ECHO = 8

        #set GPIO mode (IN / OUT)
        GPIO.setup(self.US_TRIGGER, GPIO.OUT)
        GPIO.setup(self.US_ECHO, GPIO.IN)




    def distance(self):
        # 10us is the trigger signal
        GPIO.output(self.US_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)  #10us
        GPIO.output(self.US_TRIGGER, GPIO.LOW)
        while not GPIO.input(self.US_ECHO):
            pass
        t1 = time.time()
        while GPIO.input(self.US_ECHO):
            pass
        t2 = time.time()
        time.sleep(0.01)
        return ((t2 - t1)* 340 / 2) * 100