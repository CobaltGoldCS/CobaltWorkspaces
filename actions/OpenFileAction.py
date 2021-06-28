import os, sys, subprocess
from actions.Action import Action

class OpenFileAction(Action):
    hintText = "Type in a filepath for your system"
    def run(self) -> None:
        filename = self.command
        try:
            if sys.platform == "win32":
                os.startfile(filename)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filename])
        except Exception as e:
            error(e)
