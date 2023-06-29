import pyttsx3
from threading import Thread

class TTSpeech:

    def __init__(self):
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 1)
        self.engine.setProperty('voice', "hungarian")
        self.engine = pyttsx3.init()
    
    def say(self, message):
        self.engine.say(message)
        Thread(target = self.engine.runAndWait).start()