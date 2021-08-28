from customClasses.DataClass import DataClass
from os import path
from abc import ABC, abstractmethod


class Action(ABC):
    """
    Inherit this in your custom actions

    self.command stores the user typed string from the gui\n
    For an example, look at OpenFileAction

    Override the run, it will be called when the actions are run\n
    Error will return a string that can be overriden if needed\n\n

    iconPath can be overriden in the body of the class to give a custom icon\n
    hintText can be changed the same way
    """
    
    iconPath = path.join("icons", "noImg.png")
    hintText = "This is an action"
    
    def __init__(self, command) -> None:
        self.command = command
    def __init__(self, dataclass : DataClass) -> None:
        self.dataClass = dataclass
        self.command   = dataclass.command

    
    @abstractmethod
    def run(self) -> None:
        pass
    def error(self, error : Exception) -> str:
        return f"This command is invalid; {error}"
