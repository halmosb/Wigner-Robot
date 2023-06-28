import RPi.GPIO as GPIO
import time
import json
from threading import Thread

class DotMatrix:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.running = False
        self.SCLK = 4
        self.DIO  = 14
        self.thread = ""

        with open('dot_matricies.json') as f:
            self.images = json.load(f)
      
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SCLK,GPIO.OUT)
        GPIO.setup(self.DIO,GPIO.OUT)

    def nop(self):
        time.sleep(0.00003)
        
    def start(self):
        GPIO.output(self.SCLK,0)
        self.nop()
        GPIO.output(self.SCLK,1)
        self.nop()
        GPIO.output(self.DIO,1)
        self.nop()
        GPIO.output(self.DIO,0)
        self.nop()
        
    def matrix_clear(self):
        self.matrix_display([0]*16)
        
    def send_date(self, date):
        #print(f"date:{date}")
        for i in range(0,8):
            GPIO.output(self.SCLK,0)
            self.nop()
            if date & 0x01:
                GPIO.output(self.DIO,1)
            else:
                GPIO.output(self.DIO,0)
            self.nop()
            GPIO.output(self.SCLK,1)
            self.nop()
            date >>= 1
            GPIO.output(self.SCLK,0)
        
    def end(self):
        GPIO.output(self.SCLK,0)
        self.nop()
        GPIO.output(self.DIO,0)
        self.nop()
        GPIO.output(self.SCLK,1)
        self.nop()
        GPIO.output(self.DIO,1)
        self.nop()
        
    def matrix_display(self, matrix_value):
        #print(f"matrix_vale:{matrix_value}")
        self.start()
        self.send_date(0xc0)
        
        for i in range(0,16):
            self.send_date(matrix_value[i])
            
        self.end()
        self.start()
        self.send_date(0x8A)
        self.end()
    
    def animation(self):
        if self.running:
            self.running = False
            self.thread.join()
            self.matrix_clear()
        else:
            self.thread = Thread(target = self.run_animation)
            self.thread.start()

    def run_animation(self):
        self.running = True
        while True:
            for img in self.images.keys():
                #print(img)
                self.matrix_display(self.images[img])
                time.sleep(2)
                if not self.running:
                    break
            else:
                continue
            break
    
    def show(self, name):
        self.matrix_display(self.images[name])


    def __del__(self):
        if self.running:
            self.running = False
            self.thread.join()
        self.matrix_clear()
        

if __name__ == "__main__":

    dot_matrix = DotMatrix()

    try:
        while True:
            for img in ["smile", "forward", "back", "left", "right"]:
                print(img)
                dot_matrix.matrix_display(dot_matrix.images[img])
                time.sleep(2)

        """
        while True:
            dot_matrix.matrix_display(dot_matrix.smile)
            time.sleep(1)
            dot_matrix.matrix_display(dot_matrix.matrix_back)
            time.sleep(1)
            dot_matrix.matrix_display(dot_matrix.matrix_forward)
            time.sleep(1)
            dot_matrix.matrix_display(dot_matrix.matrix_left)
            time.sleep(1)
            dot_matrix.matrix_display(dot_matrix.matrix_right)
            time.sleep(1)"""
    except KeyboardInterrupt:
        GPIO.cleanup()