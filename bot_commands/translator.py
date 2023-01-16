from .bot_command import MikuCommand
from deep_translator import GoogleTranslator

class Translator(MikuCommand):
    
    supported_languages = GoogleTranslator().get_supported_languages()
    
    def __init__(self, commandID: str):
        super().__init__(commandID)
        
    def execute(self, text_list: list):
        translate_text_idx = text_list.index('translate')
        for word in ["to", "into"]:
            if word in text_list:
                to_text_idx = ((text_list[::-1].index(word) * (-1)) -1)
        sentecne = ' '.join(text_list[translate_text_idx + 1: to_text_idx])
        to_lang = text_list[to_text_idx + 1]
        return self.__gg_translate(sentecne, to_lang)

    def __gg_translate(self, sentence: str, to_lang: str, from_lang='en') -> str:
    # print(text)
    # print(to_lang)
        if to_lang in self.supported_languages:
            translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text=sentence)
            return translated
        else:
            return 'Invalid sentences'
