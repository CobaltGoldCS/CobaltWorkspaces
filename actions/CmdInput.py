from actions.Action import Action
import os

class CmdInput(Action):
    hintText = "Type your cmd command, and it will be executed when ran"
    
    def run(self) -> None:
        try:
            os.system(self.command)
        except Exception as e:
            self.error(e)