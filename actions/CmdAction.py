from actions.Action import Action
import os

class CmdAction(Action):
    hintText = "Type your cmd command, and it will be executed when ran"
    iconPath = os.path.join("actions", "noImage.png")
    
    def run(self) -> None:
        try:
            os.system(self.command)
        except Exception as e:
            error(e)
    def error(self, error : Exception) -> str:
        return f"This Command is invalid; {error}"