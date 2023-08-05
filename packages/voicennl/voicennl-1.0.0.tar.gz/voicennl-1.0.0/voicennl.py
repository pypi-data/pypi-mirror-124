import pyttsx3 as pythonvoice
import sys, os
import random
from gtts import gTTS

class ConventorizationVoice:
    def __init__(self, path):
        self.engine = pythonvoice.init()

        with open(path, "r") as file:
            self.file = file.read()

    def voice(self):
        self.engine.say(self.file)
        self.engine.runAndWait()

    def langEN(self, filename):
        tts = gTTS(text=self.file, lang="en", slow=True)
        tts.save("{}.mp3".format(filename))

    def langDE(self, filename):
        tts = gTTS(text=self.file, lang="de", slow=True)
        tts.save("{}.mp3".format(filename))

    def langUK(self, filename):
        tts = gTTS(text=self.file, lang="uk", slow=True)
        tts.save("{}.mp3".format(filename))