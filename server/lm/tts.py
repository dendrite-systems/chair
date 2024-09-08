import pyttsx3
import time

class _TTS:
    engine = None
    rate = None
    def __init__(self):
        pass
    
    def say(self,text_):
        self.engine = pyttsx3.init()
        self.engine.say(text_)
        self.engine.runAndWait()
        del self.engine

if __name__ == "__main__":
    tts = _TTS()
    tts.say("Hello, I am a robot.")
    tts.say("I like pancakes.") 
