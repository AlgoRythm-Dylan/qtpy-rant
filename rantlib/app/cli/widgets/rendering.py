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
        buf = Buffer(width=8, height=5)
        writer = BufferWriter(buf)

        writer.write("b", fg=TermColor.Black, bg=TermColor.White)
        writer.write("r", fg=TermColor.Red)
        writer.write("g", fg=TermColor.Green)
        writer.write("y", fg=TermColor.Yellow)
        writer.write("b", fg=TermColor.Blue)
        writer.write("m", fg=TermColor.Magenta)
        writer.write("c", fg=TermColor.Cyan)
        writer.write("w", fg=TermColor.White)

        writer.add_attr(TermAttr.Bold)
        writer.write("B", fg=TermColor.Black)
        writer.write("R", fg=TermColor.Red)
        writer.write("G", fg=TermColor.Green)
        writer.write("Y", fg=TermColor.Yellow)
        writer.write("B", fg=TermColor.Blue)
        writer.write("M", fg=TermColor.Magenta)
        writer.write("C", fg=TermColor.Cyan)
        writer.write("W", fg=TermColor.White)
        writer.remove_attr(TermAttr.Bold)

        writer.write("b", bg=TermColor.Black)
        writer.write("r", bg=TermColor.Red)
        writer.write("g", bg=TermColor.Green)
        writer.write("y", bg=TermColor.Yellow)
        writer.write("b", bg=TermColor.Blue)
        writer.write("m", bg=TermColor.Magenta)
        writer.write("c", bg=TermColor.Cyan)
        writer.write("w", bg=TermColor.White, fg=TermColor.Black)
        
        writer.add_attr(TermAttr.BrightBackground)
        writer.write("B", bg=TermColor.Black)
        writer.write("R", bg=TermColor.Red)
        writer.write("G", bg=TermColor.Green)
        writer.write("Y", bg=TermColor.Yellow)
        writer.write("B", bg=TermColor.Blue)
        writer.write("M", bg=TermColor.Magenta)
        writer.write("C", bg=TermColor.Cyan)
        writer.write("W", bg=TermColor.White, fg=TermColor.Black)

        writer.write("lined", attrs=[TermAttr.Underline])

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
        if type(other) != Character:
            return False
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
            # Construct a *nix escape sequence
            bold = False
            bold_bg = False
            underline = False
            reverse = False
            for attribute in self.attributes:
                if attribute == TermAttr.Bold:
                    bold = True
                elif attribute == TermAttr.BrightBackground:
                    bold_bg = True
                elif attribute == TermAttr.Underline:
                    underline = True
                elif attribute == TermAttr.Reverse:
                    reverse = True
            bg_offset = 40
            fg_offset = 30
            if bold_bg:
                bg_offset = 100
            if bold:
                fg_offset = 90
            attr_line = f"\u001b[{fg_offset + self.foreground};{bg_offset + self.background}"
            if bold:
                attr_line += ";1"
            if underline:
                attr_line += ";4"
            if reverse:
                attr_line += ";7"
            print(f"{attr_line}m", end="")

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

    def render(self, end="\n"):
        last_character = None
        for y in range(0, self.height):
            for x in range(0, self.width):
                character = self.buffer[x + (y * self.width)]
                update_attr = last_character == None or not last_character.same_formatting_as(character)
                if update_attr:
                    TerminalFunctions.reset()
                    character.apply_attributes()
                if character.char == None:
                    print(" ", end="")
                else:
                    print(character.char, end="")
                if update_attr:
                    TerminalFunctions.flush()
                last_character = character
            TerminalFunctions.reset()
            if not y == self.height - 1:
                TerminalFunctions.newline_flush()
            else:
                print(end, end="")

class BufferWriter:

    def __init__(self, buffer):
        self.buffer = buffer
        self.x = 0
        self.y = 0
        self.attrs = []
        self.foreground = TermColor.White
        self.background = TermColor.Black

    def add_attr(self, attr):
        if not attr in self.attrs:
            self.attrs.append(attr)
            self.attrs.sort()

    def remove_attr(self, attr):
        self.attrs.remove(attr)

    def reset_attrs(self):
        self.attrs = []

    def write(self, text, fg=None, bg=None, attrs=None):
        if fg == None:
            fg = self.foreground
        if bg == None:
            bg = self.background
        if attrs == None:
            attrs = self.attrs
        else:
            attrs.sort()
        for char in text:
            if text == "\n" or self.x == self.buffer.width:
                self.x = 0
                self.y += 1
            if self.y == self.buffer.height:
                break
            c = self.buffer.get_at(self.x, self.y)
            c.foreground = fg
            c.background = bg
            c.char = char
            c.attributes = attrs[:] # Shallow copy should be good
            self.x += 1


if __name__ == "__main__":
    TerminalFunctions.test_page()