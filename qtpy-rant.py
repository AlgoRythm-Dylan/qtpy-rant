import os
import sys
import argparse

# Append current directory to PYTHONPATH to load our libraries
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

# Check to make sure all packages are installed correctly, if not, die
try:
    import requests
    from PyQt5.QtWidgets import QApplication
except ImportError as ex:
    print("[qtpy-rant]: Could not import packages (Are they installed?)", file=sys.stderr)
    print(ex, file=sys.stderr)
    sys.exit(1)

class QtPyApp:

    def __init__(self):
        self.gui_mode = True


def main():

    application = QtPyApp()

    argp = argparse.ArgumentParser(description="The hackable, plugin-able, Qt-based, Python-powered devRant client")
    argp.add_argument("--nogui", type=bool, choices=[True, False], default=False, help="Start in CLI mode. qtpy-rant becomes just py-rant")
    args = argp.parse_args()
    
    application.gui_mode = not args.nogui


if __name__ == "__main__":
    main()