import speech_recognition as sr
import speech2text
import command_checker
from bot_commands import *

def main():
    recognizer = sr.Recognizer()
    # commands init
    checker = command_checker.CommandChecker("miku_responses.json")
    checker.add_command(translator.Translator("translation"))
    checker.add_command(spotifyskill.SpotifyObject("spotify"))
    checker.add_command(led_control.LEDControl("ledControl"))
    while True:
        try:
            user_input = speech2text.listening(recognizer)
            # user_input = input("Enter command: ")
            if user_input == "stop operation":
                break
            checker.check_command(user_input)
            # print(checker.commands)
            
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            continue


if __name__ == "__main__":
    main()
