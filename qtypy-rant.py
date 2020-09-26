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

class Application:

    def __init__(self):
        pass


def main():
    pass

if __name__ == "__main__":
    main()