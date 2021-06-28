from customClasses.DataClass import DataClass
from os import path
from abc import ABC, abstractmethod
class Action(ABC):
    """Inherit this in your custom actions

    self.command stores the user typed string from the gui\n
    For an example, look at OpenFileAction
    """
    iconPath = path.join("icons", "noImage.png")
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
        return error
