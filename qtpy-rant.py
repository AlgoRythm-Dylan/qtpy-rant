import os
import sys
import argparse
from pathlib import Path

# Append current directory to PYTHONPATH to load our libraries
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from rantlib.core_application.nogui.client import TerminalClient
from rantlib.core_application.ui.client import QtClient

class QtPyApp:

    def __init__(self):
        self.gui_mode = True
        self.args = None
        self.client = None
        self.current_user = None

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

    argp = argparse.ArgumentParser(description="The hackable, plugin-able, Qt-based, Python-powered devRant client")
    argp.add_argument("--nogui", action="store_true", help="Start in CLI mode. qtpy-rant becomes just py-rant")
    argp.add_argument("--theme-tool", action="store_true", help="Open the theme tool for creating and editing themes")
    qtpy.args = argp.parse_args()

    qtpy.gui_mode = not qtpy.args.nogui

    start_app(qtpy)


if __name__ == "__main__":
    main()