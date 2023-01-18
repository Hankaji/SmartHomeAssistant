from gpiozero import LED, exc
from .bot_command import MikuCommand
import time

class LEDControl(MikuCommand):
    
    def __init__(self, commandID: str):
        super().__init__(commandID)
        try:
            self.green_LED = LED(21)
            self.yellow_LED = LED(20)
            self.red_LED = LED(16)
            self.led_dict = {"green": self.green_LED,
                            "yellow": self.yellow_LED,
                            "red": self.red_LED}
        except exc.BadPinFactory:
            print("couldnt connect to raspberry pi")
        self.led_id = ["green", "yellow", "red"]
        self.led_responses = ["green light", "yellow light", "red light"]
        
    def __get_response(self, led_state: str, res_index: int) -> str:
        if led_state == "on":
            return "turning on " + self.led_responses[res_index]
        elif led_state == "off":
            return "turning off " + self.led_responses[res_index]
    
    def execute(self, text_list: list) -> str:
        response = ""
        led_toggle_count = 0
        for index, led_color in enumerate(self.led_id):
            if led_color in text_list:
                if "on" in text_list:
                    if led_toggle_count < 1:
                        response += self.__get_response("on", index)
                    else:
                        response += " and " + self.__get_response("on", index)
                    try:
                        self.led_dict.get(led_color).on()
                    except AttributeError:
                        print("no LED pin was found on raspberry pi, make sure you have it connected")
                elif "off" in text_list:
                    if led_toggle_count < 1:
                        response += self.__get_response("off", index)
                    else:
                        response += " and " + self.__get_response("off", index)
                    try:
                        self.led_dict.get(led_color).off()
                    except AttributeError:
                        print("no LED pin was found on raspberry pi, make sure you have it connected")
                led_toggle_count += 1
        return response
