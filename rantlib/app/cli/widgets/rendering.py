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

class TermColor:
    Black = 0
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4
    Magenta = 5
    Cyan = 6
    White = 7

class TermAttr:
    Bold = 0
    BrightBackground = 1
    Reverse = 2
    Underline = 3

if windows_mode:
    # Windows translation object
    class WindowsTranslate:
        BackgroundColor = [
            windows_bg["black"],
            windows_bg["red"],
            windows_bg["green"],
            windows_bg["yellow"],
            windows_bg["blue"],
            windows_bg["magenta"],
            windows_bg["cyan"],
            windows_bg["white"]
        ]
        ForegroundColor = [
            windows_fg["black"],
            windows_fg["red"],
            windows_fg["green"],
            windows_fg["yellow"],
            windows_fg["blue"],
            windows_fg["magenta"],
            windows_fg["cyan"],
            windows_fg["white"]
        ]
        Attributes = [
            0x0008,
            0x0080,
            0x4000,
            0x8000
        ]

class TerminalFunctions:

    @staticmethod
    def newline_flush():
        print("")
        TerminalFunctions.flush()

    @staticmethod
    def flush():
        sys.stdout.flush()

    @staticmethod
    def test_page():
        buf = Buffer(width=10, height=4)
        buf.get_at(0, 0).char = "R"
        buf.get_at(0, 0).foreground = TermColor.Red
        buf.render()

    @staticmethod
    def reset():
        if windows_mode:
            default_attrs = WindowsTranslate.ForegroundColor[TermColor.White] | WindowsTranslate.BackgroundColor[TermColor.Black]
            windows_SetConsoleTextAttribute(windows_stdout(), default_attrs)
        else:
            print(f"\u001b[00m", end="")



class Character:

    def __init__(self, char=None):
        self.char = char
        self.background = TermColor.Black
        self.foreground = TermColor.White
        self.attributes = []

    def __eq__(self, other):
        return self.char == other.char and self.same_formatting_as(other)

    def same_formatting_as(self, other):
        if len(self.attributes) != len(other.attributes):
            return False
        # Attributes is assumed to be a sorted list. Please
        # use add_attr and remove_attr rather than modifying
        # attributes array directly
        for i in range(0, len(self.attributes)):
            if self.attributes[i] != other.attributes[i]:
                return False
        # At this point, the attributes have been checked and
        # the only remaining point of contest is the colors
        return self.background == other.background and self.foreground == other.foreground

    def add_attr(self, attr):
        if not attr in self.attributes:
            self.attributes.append(attr)
            self.attributes.sort()

    def remove_attr(self, attr):
        self.attributes.remove(attr)

    def apply_attributes(self):
        if windows_mode:
            attr_int = WindowsTranslate.ForegroundColor[self.foreground] | WindowsTranslate.BackgroundColor[self.background]
            for attribute in self.attributes:
                attr_int |= WindowsTranslate.Attributes[attribute]
            windows_SetConsoleTextAttribute(windows_stdout(), attr_int)
        else:
            bold = TermAttr.Bold in self.attributes
            bold_bg = TermAttr.BrightBackground in self.attributes
            # Forground *nix color code
            print(f"\u001b[{self.foreground}{'1' if bold else ''}m", end="")
            # Backgound *nix color code
            print(f"\u001b[{self.background};{'1' if bold_bg else ''}m", end="")
            # *nix attributes
            if TermAttr.Underline in self.attributes:
                print("\u001b[4m", end="")
            if TermAttr.Reverse in self.attributes:
                print("\u001b[7m", end="")

class Buffer:

    def __init__(self, width=0, height=0):
        self.resize(width, height)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.buffer = [Character() for i in range(width * height)]

    def add_line(self):
        self.height += 1
        for x in range(0, self.width):
            self.buffer.append(Character())

    def __getitem__(self, key):
        return self.buffer[key]

    def __iter__(self):
        return self.buffer.__iter__()

    def __setitem__(self, key, value):
        self.buffer[key] = value

    def set_at(self, x, y, value):
        self.buffer[x + (y + self.width)] = value

    def get_at(self, x, y):
        return self.buffer[x + (y * self.width)]

    def render(self):
        last_character = None
        for y in range(0, self.height):
            for x in range(0, self.width):
                character = self.buffer[x + (y * self.height)]
                update_attr = last_character == None or not last_character.same_formatting_as(character)
                if update_attr:
                    character.apply_attributes()
                if character.char == None:
                    print(" ", end="")
                else:
                    print(character.char, end="")
                if update_attr:
                    TerminalFunctions.flush()
                last_character = character
            TerminalFunctions.reset()
            TerminalFunctions.newline_flush()