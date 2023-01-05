import speech_recognition as sr

def listening(recognizer: sr.Recognizer):
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, 0.2)
        audio = recognizer.listen(mic)

        text: str = recognizer.recognize_google(audio)
        text.lower().capitalize()

        print(f"Recognized {text}")
        return text.lower()
