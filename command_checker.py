import json
import re
import random
from bot_commands.bot_command import MikuCommand

class CommandChecker():
    
    def __init__(self, response_json) -> None:
        # initialization
        with open(response_json, "r") as f:
            self.responses = json.loads(f.read())
        self.commands = []
        self.command_IDs = []
    
    def add_command(self, command_object: MikuCommand):
        if command_object not in self.commands:
            self.commands.append(command_object)
            self.command_IDs.append(command_object.commandID)
            
    def __get_best_response(self, arr_value: list):
        highest_score = max(arr_value)
        best_responses = self.responses[arr_value.index(highest_score)]["response"]
        return random.choice(best_responses)

    def check_command(self, phrase: str):
        text_list = re.split(r"\s+|[-?!.,;]\s*", phrase)
        score = []
        for response in self.responses:
            response_score = 0  # Check for the likelihood of the response
            keyword_score = 0  # Check if command meet the reqquired conditions
            # Checking if there are required keywords are not
            if response["requiredKeyword"]:
                for keyword in response["requiredKeyword"]:
                    if keyword is not list and keyword in text_list:
                        keyword_score += 1
                    elif keyword is list:
                        for keyword_OR in keyword:
                            if keyword_OR in text_list:
                                keyword_score += 1
                                break
            
            # Continue if there are sufficient required kws otherwise skip
            if keyword_score == len(response["requiredKeyword"]):
                for word in text_list:
                    if word in response["userInput"]:
                        response_score += 1
                        
            score.append(response_score / len(text_list))
        
        best_response = self.__get_best_response(score)
        print(score)
        print("bot: " + best_response)

