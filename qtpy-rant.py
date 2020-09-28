import os
import sys
import argparse

# Append current directory to PYTHONPATH to load our libraries
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

# Check to make sure all pip packages are installed correctly, if not, die
try:
    import requests
    from PyQt5.QtWidgets import QApplication
except ImportError as ex:
    print("[qtpy-rant]: Could not import packages (Are they installed?)", file=sys.stderr)
    print(ex, file=sys.stderr)
    sys.exit(1)

from rantlib.core_application.ui.mainwindow import MainWindow
from rantlib.core_application.nogui.client import TerminalDevRantClient
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
    qtpy.client.qapplication = QApplication(sys.argv)
    qtpy.client.main_window = MainWindow()
    qtpy.client.main_window.show()

def start_cli(qtpy):
    qtpy.client = TerminalDevRantClient(qtpy)

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
    qtpy.args = argp.parse_args()

    qtpy.gui_mode = not qtpy.args.nogui

    start_app(qtpy)


if __name__ == "__main__":
    main()