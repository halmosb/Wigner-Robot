import RPi.GPIO as GPIO
import time



class Motor:
    """
    
    """

    class Pin:
        def __init__(self, forward_pin, backward_pin, pwm_pin, frequency):
            self.forward_pin = forward_pin
            self.backward_pin = backward_pin
            self.frequency = frequency
            self.pwm_pin = pwm_pin

            GPIO.setup(self.forward_pin,GPIO.OUT)
            GPIO.setup(self.backward_pin,GPIO.OUT)
            GPIO.setup(self.pwm_pin,GPIO.OUT)

            self.pwm = GPIO.PWM(self.pwm_pin,self.frequency)
            self.pwm.start(0)


    def __init__(self, frequency=100):

        self.frequency = frequency

        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)  # use BCM numbers

        self.motors = {
            "UL": self.Pin(21, 20, 0, self.frequency),
            "LL": self.Pin(22, 23, 1, self.frequency),
            "UR": self.Pin(24, 25, 12, self.frequency),
            "LR": self.Pin(27, 26, 13, self.frequency)
        }

    def __del__(self):
        self.set_speed(0)
        GPIO.cleanup()

    def set_speed(self, speed):
        """
        """
        if type(speed) is dict:
            for name, pins in self.motors.items():
                sp = speed[name]
                #print(name, pins, sp)
                if sp > 0:
                    GPIO.output(pins.backward_pin, GPIO.LOW)
                    GPIO.output(pins.forward_pin, GPIO.HIGH)
                    pins.pwm.ChangeDutyCycle(sp)
                elif sp < 0:
                    GPIO.output(pins.forward_pin, GPIO.LOW)
                    GPIO.output(pins.backward_pin, GPIO.HIGH)
                    pins.pwm.ChangeDutyCycle(-sp)
                else:
                    GPIO.output(pins.forward_pin, GPIO.LOW)
                    GPIO.output(pins.backward_pin, GPIO.LOW)
                    pins.pwm.ChangeDutyCycle(0)
        elif type(speed) is int:
            sp = {
                "UL": speed,
                "LL": speed,
                "UR": speed,
                "LR": speed
            }
            self.set_speed(sp)


            
if __name__ == "__main__":
    motors = Motor()

    speed = {
        "UL": 20,
        "LL": 20,
        "UR": 20,
        "LR": 20
    }

    motors.set_speed(speed)

    time.sleep(1)

    #motors.set_speed(0)

