# This section includes code for cross platform terminal
# control over color and attributes

import sys

windows_mode = True

try:
    # Try to import Windows libs. If failure, we can guess this
    # is *nix
    import ctypes
    from ctypes import LibraryLoader
    windll = LibraryLoader(ctypes.WinDLL)
    from ctypes import wintypes
except (AttributeError, ImportError):
    windows_mode = False

# Bind some required c WinAPI functions to python
if windows_mode:
    # Returns stdout handle
    windows_GetStdHandle = windll.kernel32.GetStdHandle
    windows_GetStdHandle.argtypes = [
        wintypes.DWORD
    ]
    windows_GetStdHandle.restype = wintypes.HANDLE

    def windows_stdout():
        # Thank c for this magic number
        return windows_GetStdHandle(-11)

    # Sets text attributes, much like ncurses attron function
    windows_SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    windows_SetConsoleTextAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD
    ]
    windows_SetConsoleTextAttribute.restype = wintypes.BOOL

    # Foreground and background colors in Windows have different values
    windows_fg = {
        "black": 0x0000,
        "red": 0x0004,
        "green": 0x0002,
        "blue": 0x0001
    }

    # This may be more slow, technically, but it's more readable.
    windows_fg["magenta"] = windows_fg["blue"] | windows_fg["red"]
    windows_fg["yellow"] = windows_fg["red"] | windows_fg["green"]
    windows_fg["cyan"] = windows_fg["green"] | windows_fg["blue"]
    windows_fg["white"] = windows_fg["green"] | windows_fg["blue"] | windows_fg["red"]

    # Repeat the process for bg colors. They're basically just one order of
    # magnitude higher.
    windows_bg = {
        "black": 0x0000,
        "red": 0x0040,
        "green": 0x0020,
        "blue": 0x0010,
    }

    windows_bg["magenta"] = windows_bg["blue"] | windows_bg["red"]
    windows_bg["yellow"] = windows_bg["red"] | windows_bg["green"]
    windows_bg["cyan"] = windows_bg["green"] | windows_bg["blue"]
    windows_bg["white"] = windows_bg["green"] | windows_bg["blue"] | windows_bg["red"]  

from enum import Enum

# The order on this enum is important,
# they are the order of the ASCII colors and convert to
# linux 1:1
TermColor = Enum(
    'Black',
    'Red',
    'Green',
    'Yellow',
    'Blue',
    'Magenta',
    'Cyan',
    'White'
)

TermAttr = Enum(
    'Bold',
    'BrightBackground',
    'Underline',
    'Reverse'
)

class Character:

    def __init__(self, char=None):
        self.char = char
        self.background = None
        self.foreground = None
        self.attributes = []

class Buffer:

    def __init__(self, width=0, height=0):
        self.buffer = [Character()] * (width * height)

    def render(self):
        pass

    def apply_attributes(self, attributes):
        for attribute in attributes:
            if attribute == TermAttr.Bold: