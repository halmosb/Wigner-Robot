import RPi.GPIO as GPIO
import time
from threading import Thread


class Buzzer():
    def __init__(self, volume = 50, tempo = 120):
        self.pin = 16
        self.volume = volume
        self.tempo = tempo


        GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
        GPIO.setup(self.pin, GPIO.OUT)    # Set pins' mode is output 
        self.buzz = GPIO.PWM(self.pin, 440)    # 440 is initial frequency.

    def playlist(self):
        self.buzz.start(self.volume)
        for i in range(0, len(self.song)):     # Play song 1
            self.buzz.ChangeFrequency(self.song[i][0]) # Change the frequency along the song note
            time.sleep(self.song[i][1] * 60/self.tempo)
        self.buzz.stop()

    def play(self, song):
        self.song = song
        self.thread = Thread(target = self.playlist)
        self.thread.start()
