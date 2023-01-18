from abc import ABC, abstractmethod

class MikuCommand(ABC):

    def __init__(self, commandID: str):
        self.commandID = commandID

    @abstractmethod
    def execute(self, text_list: list) -> str:
        pass