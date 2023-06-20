import pttsx3
from threading import Thread

class TTSpeech:

    def __init__(self):
        self.engine = pttsx3.init()
    
    def say(self, message):
        self.engine.say(message)
        Thread(target = self.engine.runAndWait).start()