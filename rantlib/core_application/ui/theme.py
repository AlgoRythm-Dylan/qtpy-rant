import requests
import json
from rantlib.core_application.storage import read_data_file
from os import walk
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidgetItem
from pathlib import Path

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
        self.vote_foreground = None
        self.vote_background = None


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
        self.accent_foreground = data.get("accent_foreground", "#ffffff")
        self.secondary_background = data.get("secondary_background", "#40415a")
        self.secondary_foreground = data.get("secondary_foreground", "#ffffff")
        self.vote_background = data.get("vote_background", "#ccccd4")
        self.vote_foreground = data.get("vote_foreground", "#ffffff")

def qss(styles, apply_to="*"):
    qss_str = f"{apply_to}" + "{"
    for style in styles.keys():
        qss_str += f"{style}: {styles[style]};"
    return qss_str + "}"

def apply_theme_to_widget(client, element, theme):
    try:
        name = get_theme_class_name(element.objectName())
    except:
        return # Can't theme this item
    if name == "devrant_window" or name == "devrant_panel":
        element.setStyleSheet(qss({
            "background-color": theme.background,
            "color": theme.foreground,
            "font-size": "20px",
            "font-family": "Roboto"
        }))
    elif name == "devrant_secondary_panel":
        element.setStyleSheet(qss({
            "background-color": theme.secondary_background,
            "color": theme.secondary_foreground,
            "font-size": "20px",
            "font-family": "Roboto"
        }))
    elif name == "devrant_alt_label":
        element.setStyleSheet(qss({
            "color": theme.foreground_alt,
            "font-size": "20px",
            "font-family": "Roboto"
        }))
    elif name == "devrant_button":
        element.setStyleSheet(qss({
            "background-color": theme.accent_background,
            "color": theme.accent_foreground,
            "border": "none",
            "border-radius": "10px",
            "padding": "10px",
            "font-size": "20px",
            "font-family": "Roboto"
        }))
        element.setCursor(Qt.PointingHandCursor)
    elif name == "devrant_vote_button":
        element.setStyleSheet(qss({
            "background-color": theme.vote_background,
            "color": theme.vote_foreground,
            "border": "none",
            "border-radius": "20px",
            "height": "40px",
            "width": "40px",
            "max-height": "40px",
            "max-width": "40px",
            "font-family": "Comfortaa",
            "font-size": "20px",
            "padding": "0px"
        }))
        element.setCursor(Qt.PointingHandCursor)
    elif name == "devrant_title_label":
        element.setStyleSheet(qss({
            "font-family": "Comfortaa",
            "font-size": "30px",
            "margin": "0px",
            "padding": "0px"
        }))

def apply_theme(client, root_element, theme=None):
    if theme == None:
        theme = client.theme
    layout = root_element.layout()
    if layout != None:
        apply_theme_to_widget(client, root_element, theme)
        for i in range(0, layout.count()):
            apply_theme(client, layout.itemAt(i), theme)
    elif type(root_element) == QWidgetItem:
        apply_theme(client, root_element.widget(), theme)
    else:
        apply_theme_to_widget(client, root_element, theme)

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
        return get_theme_class_name(item.objectName())

def get_theme_directory():
    return Path(__file__).parent.parent.parent.parent.joinpath("themes")

def load_theme(file_name):
    theme = Theme()
    theme.data(read_data_file(get_theme_directory().joinpath(file_name), default={}))
    return theme

def load_themes():
    theme_directory = get_theme_directory()
    themes = []
    for dirpath, dirnames, filenames in walk(theme_directory):
        for file in filenames:
            if file.lower().endswith(".json") and file != "web_themes.json":
                theme = Theme()
                theme_path = Path(theme_directory).joinpath(file)
                theme.data(read_data_file(theme_path, default={}))
                theme.source = theme_path
                themes.append(theme)
        break
    return themes

def source_name(self):
    return Path(self.source).name