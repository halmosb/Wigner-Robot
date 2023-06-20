import RPi.GPIO as GPIO
import time
from threading import Thread
from control import Control

class Sensor:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.US_TRIGGER = 9
        self.US_ECHO = 8

        #set GPIO mode (IN / OUT)
        GPIO.setup(self.US_TRIGGER, GPIO.OUT)
        GPIO.setup(self.US_ECHO, GPIO.IN)
        self.thread = None

        self.start_thread()

    def start_thread(self):
        self.thread = Thread(target = self.measuring)
        self.thread.start()

    def measuring(self):
        while (Control.sensor):
            Control.distance = self.distance()
            time.sleep(0.05)

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
        #time.sleep(0.01)
        #print(((t2 - t1)* 340 / 2) * 100)
        return ((t2 - t1)* 340 / 2) * 100