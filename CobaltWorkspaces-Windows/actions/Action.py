from customClasses.DataClass import DataClass
from os import path
class Action():
    iconPath = path.join("actions", "noImage.png")
    hintText = "This is an action"
    def __init__(self, command):
        self.command = command
    def __init__(self, dataclass : DataClass):
        self.dataClass = dataclass
        self.command = dataclass.command
    
    def run(self, value : str) -> None:
        pass
    def error(self, error : Exception) -> str:
        pass
