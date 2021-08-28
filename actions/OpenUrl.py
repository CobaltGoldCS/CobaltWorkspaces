from actions.Action import Action
import webbrowser
from os import path


class OpenUrl(Action):
    hintText = "Type the url you want to visit"

    def run (self) -> None:
        try:
            url = self.command
            if not url.startswith("http"): url = "http://" + url
            
            webbrowser.get("windows-default").open(url, 2)
        except Exception as e:
            self.error(e)
    def error(self, error : Exception) -> str:
        return f"This url cannot be opened; {error}"