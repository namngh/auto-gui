from .error import INVALID_URI
from .utils import uri_validator
import webbrowser

class Browser(object):
    def __init__(self, **data):
        # List support browser https://docs.python.org/3/library/webbrowser.html
        self.browser = data.get("browser", None)
        self.url = data.get("url")

        if not uri_validator(self.url):
            raise Exception(INVALID_URI)

        if self.url[-1] == "/":
            self.url = self.url[:-1]

    def open(self):
        if self.browser == None:
            webbrowser.open(self.url)
        else:
            webbrowser.get(self.browser).open(self.url)