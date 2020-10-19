import os
import sys
import argparse
from pathlib import Path

# Append current directory to PYTHONPATH to load our libraries
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

VERSION = "0.1.0"

from rantlib.core_application.nogui.client import TerminalClient
from rantlib.core_application.ui.client import QtClient
from rantlib.core_application.event.event import EventEmitter
from rantlib.core_application.auth import AuthService
from rantlib.core_application.config import QtPyRantConfig
from rantlib.core_application.lang import load_language
from rantlib.core_application.storage import STD_PATH_APP_CONFIG

class QtPyApp(EventEmitter):

    def __init__(self):
        super().__init__()
        self.gui_mode = True
        self.args = None
        self.client = None
        self.current_user = None
        self.config = QtPyRantConfig()
        self.config.read_data_file(STD_PATH_APP_CONFIG)
        self.language = load_language(self.config.get("language"))
        self.auth_service = AuthService()

    def is_guest_mode(self):
        return self.current_user == None

def start_gui(qtpy):
    qtpy.client = QtClient(qtpy)

def start_cli(qtpy):
    qtpy.client = TerminalClient(qtpy)

def start_app(qtpy):
    if qtpy.gui_mode:
        start_gui(qtpy)
    else:
        start_cli(qtpy)
    qtpy.client.run()

def main():

    qtpy = QtPyApp()

    argp = argparse.ArgumentParser(description=qtpy.language.get("app_short_desc"))
    argp.add_argument("--nogui", action="store_true", help=qtpy.language.get("app_arg_nogui_help"))
    argp.add_argument("--theme-tool", action="store_true", help=qtpy.language.get("app_arg_theme_tool_help"))
    qtpy.args = argp.parse_args()

    qtpy.gui_mode = not qtpy.args.nogui

    start_app(qtpy)


if __name__ == "__main__":
    main()