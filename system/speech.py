import pyttsx3
from threading import Thread

class TTSpeech:

    def __init__(self):
        self.engine = pyttsx3.init()
    
    def say(self, message):
        self.engine.say(message)
        Thread(target = self.engine.runAndWait).start()