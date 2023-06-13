import RPi.GPIO as GPIO
import time
from threading import Thread
import json



class Buzzer():
    def __init__(self, volume = 50):
        self.pin = 16
        self.volume = volume
        self.running = False
        
        with open('songs.json') as f:
            self.songs = json.load(f)


        GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
        GPIO.setup(self.pin, GPIO.OUT)    # Set pins' mode is output 
        self.buzz = GPIO.PWM(self.pin, 440)    # 440 is initial frequency.

    def playlist(self):
        self.running = True
        self.buzz.start(self.volume)
        for i in range(0, len(self.song)):     # Play song 1
            self.buzz.ChangeFrequency(self.song[i][0]) # Change the frequency along the song note
            time.sleep(self.song[i][1])
            if not self.running:
                break
        self.buzz.stop()

    def play_whole(self):
        if self.running:
            self.running = False
        else:
            self.song = []
            for s in self.songs:
                self.song.append(s)
            self.thread = Thread(target = self.playlist)
            self.thread.start()

    def play(self, song):
        try:
            self.song = self.songs[song]
        except: 
            self.song=[[880,5]]
        self.thread = Thread(target = self.playlist)
        self.thread.start()
    
    def __del__(self):
        self.running = False
