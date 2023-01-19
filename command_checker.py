import json
import re
import random
import pyttsx3
from subprocess import call
from bot_commands.bot_command import MikuCommand

class CommandChecker():
    
    def __init__(self, response_json) -> None:
        # initialization
        with open(response_json, "r") as f:
            self.responses = json.loads(f.read())
        self.speech_engine = pyttsx3.init()
        # self.zira_en_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        # self.haruka_jp_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0"
        # self.speech_engine.setProperty('rate', 124)
        self.cmd_en_beg = r"./enspeech.sh"
        self.cmd_ja_beg = r"./jaspeech.sh"
        self.commands = []
        self.command_IDs = []
    
    def add_command(self, command_object: MikuCommand):
        if command_object not in self.commands:
            self.commands.append(command_object)
            self.command_IDs.append(command_object.commandID)
            
    def __get_best_response(self, arr_value: list):
        highest_score = max(arr_value)
        best_responses = self.responses[arr_value.index(highest_score)]["response"]
        return random.choice(best_responses), arr_value.index(highest_score)
    
    def __check_word_list(self, phrase_list: list, keyword_list: list):
        similar_word = 0  # check for the similarity count
        for keyword in keyword_list:
            # Since there are nested list (represent as OR kw) in keyword list
            # This statement check whether the element is a list or not
            if type(keyword) is not list and keyword in phrase_list:
                # print(f"detect kw: {keyword}")
                similar_word += 1
            elif type(keyword) is list:
                for keyword_OR in keyword:
                    # Either any keyword in the nested list found will break this for loop
                    if keyword_OR in phrase_list:
                        # print(f"detect kw_or: {keyword_OR}")
                        similar_word += 1
                        break
        
        return similar_word

    def check_command(self, phrase: str):
        text_list = re.split(r"\s+|[-?!.,;]\s*", phrase.lower())
        score = []
        for response in self.responses:
            response_score = 0  # Calculating the likelihood of the response
            keyword_score = 0  # Check if command meet the reqquired conditions
            keywords = response["requiredKeyword"]
            input_type = response["inputType"]
            # Checking if there are required keywords are not
            if keywords:
                keyword_score += self.__check_word_list(text_list, keywords)

            # Continue if there are sufficient required kws otherwise skip
            if keyword_score == len(keywords):
                response_score += self.__check_word_list(text_list, response["userInput"])
                # Convert to the percentage of matching words
                response_score = response_score / len(text_list)
                # Responses with required keywords are more important thus have more priority
                if keywords:
                    response_score += 0.5
                # Responses with the type "command" should be priotize more than other types
                if input_type == "command":
                    response_score += 1

            score.append(response_score)
        
        if max(score) == 0: 
            print("couldnt understand")
            return
        best_response, response_idx = self.__get_best_response(score)
        print(score)
        # Start finding and executing command if inputType is command
        bot_line = ""
        if self.responses[response_idx]["inputType"] == "command":
            # print(self.responses[response_idx])
            # print("detect command input type")
            bot_line = self.__find_command(self.responses[response_idx]["commandID"], text_list)
        bot_response = f"{best_response} {bot_line}"
        # print(self.speech_engine.getProperty('voices'))
        print("bot: " + bot_response)
        self.__text2speech(text_list, bot_response)
        
        
    # language  : en_US, de_DE, ...
    # gender    : VoiceGenderFemale, VoiceGenderMale
    # def change_voice(self, engine, language, gender='VoiceGenderFemale'):
    #     for voice in engine.getProperty('voices'):
    #         print(voice)
    #         if language in voice.languages and gender == voice.gender:
    #             engine.setProperty('voice', voice.id)
    #             return True

    #     raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
    
    # def change_voice(self, engine, language_id):
    #         engine.setProperty('voice', language_id)
        
    # def __text2speech(self, original_sentence, sentence_to_say):
    #     if 'japanese' in original_sentence:
    #         self.change_voice(self.speech_engine, self.haruka_jp_id)
    #     else:
    #         self.change_voice(self.speech_engine, self.zira_en_id)
    #     self.speech_engine.say(sentence_to_say)
    #     self.speech_engine.runAndWait()
    
    def gg_tts(self, original_sentence, sentence_to_say):
        if 'japanese' in original_sentence:
            # self.change_voice(self.speech_engine, self.haruka_jp_id)
            call([self.cmd_ja_beg + " " + sentence_to_say], shell=True)
        else:
            # self.change_voice(self.speech_engine, self.zira_en_id)
            call([self.cmd_en_beg + " " + sentence_to_say], shell=True)

    def __find_command(self, commandID, text_list):
        if commandID not in self.command_IDs:
            print(f"No command found in the list, make sure you have added it")
            return
        
        # Find the index of the command
        cmd_index = self.command_IDs.index(commandID)
        # Execute command via index
        return self.commands[cmd_index].execute(text_list)
        

