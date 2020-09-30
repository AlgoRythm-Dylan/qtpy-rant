import requests
import json
from rantlib.core_application.data.storage import read_data_file

class Theme:

    def __init__(self):
        self.title = None
        self.description = None
        self.authors = None
        self.source = None

        self.background = None
        self.foreground = None
        self.foreground_alt = None
        self.accent_background = None
        self.accent_foreground = None
        self.secondary_background = None
        self.secondary_foreground = None


    def load(self, source=None):
        if source == None:
            source = self.source
        self.source = source
        if source.lower().startswith("http://") or source.lower().startswith("https://"):
            self.data(requests.get(source).json()) # Load over HTTP(S)
        else:
            self.data(read_data_file(source, default={}))


    def data(self, data):
        self.title = data.get("title", "<No Title Provided>")
        self.description = data.get("description", "<No Description Provided>")
        self.authors = data.get("authors", "<No Authors Provided>")

        self.background = data.get("background", "#ffffff")
        self.foreground = data.get("foreground", "#2f2f32")
        self.foreground_alt = data.get("foreground_alt", "#aaaab8")
        self.accent_background = data.get("accent_background", "#d55161")
        self.accent_foregruond = data.get("accent_foreground", "#ffffff")
        self.secondary_background = data.get("secondary_background", "#40415a")
        self.secondary_foreground = data.get("secondary_foreground", "#ffffff")


def apply_theme(root_element, theme):
    pass

def get_theme_class_name(item):
    if type(item) == str:
        # Expected like <class name>#<object id>
        char_pos = item.find("#")
        if char_pos == -1:
            return item
        else:
            return item[:char_pos]
    else:
        # This is assumed to be a Qt Object
        return get_theme_class_name(item.getObjectName())