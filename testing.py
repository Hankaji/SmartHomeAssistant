import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 124)

for voice in engine.getProperty('voices'):
    print(voice)