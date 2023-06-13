import RPi.GPIO as GPIO
import time
import json

class DotMatrix:

    def __init__(self):

        print("Starting led matrix")

        self.SCLK = 8
        self.DIO  = 9

        self.smile = json.load("dot_matricies")["smile"]
        #self.smile = (0x00, 0x00, 0x38, 0x40, 0x40, 0x40, 0x3a, 0x02, 0x02, 0x3a, 0x40, 0x40, 0x40, 0x38, 0x00, 0x00)
        self.matrix_forward = (0x00, 0x00, 0x00, 0x00, 0x12, 0x24, 0x48, 0x90, 0x90, 0x48, 0x24, 0x12, 0x00, 0x00, 0x00, 0x00)
        self.matrix_back = (0x00, 0x00, 0x00, 0x00, 0x48, 0x24, 0x12, 0x09, 0x09, 0x12, 0x24, 0x48, 0x00, 0x00, 0x00, 0x00)
        self.matrix_left = (0x00, 0x00, 0x00, 0x00, 0x18, 0x24, 0x42, 0x99, 0x24, 0x42, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00)
        self.matrix_right = (0x00, 0x00, 0x00, 0x00, 0x00, 0x81, 0x42, 0x24, 0x99, 0x42, 0x24, 0x18, 0x00, 0x00, 0x00, 0x00)

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
        GPIO.output(self.SCLK,0)
        self.nop()
        GPIO.output(self.DIO,0)
        self.nop()
        GPIO.output(self.DIO,0)
        self.nop()
        
    def send_date(self, date):
        print(f"date:{date}")
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
        print(f"matrix_vale:{matrix_value}")
        self.start()
        self.send_date(0xc0)
        
        for i in range(0,16):
            self.send_date(matrix_value[i])
            
        self.end()
        self.start()
        self.send_date(0x8A)
        self.end()

if __name__ == "__main__":

    dot_matrix = DotMatrix()

    try:
        dot_matrix.matrix_display(dot_matrix.smile)
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