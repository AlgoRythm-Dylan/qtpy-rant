# This file, full of awful, hacky code, is now illegal.
# It will be deleted when the rest of the project works without it.

"""

import sys

windows_mode = False
stdout = -11
try:
    import ctypes
    from ctypes import LibraryLoader
    windll = LibraryLoader(ctypes.WinDLL)
    from ctypes import wintypes
    windows_mode = True
except (AttributeError, ImportError):
    windows_mode = False # Just to be sure, I guess...

if windows_mode:
    windows_GetStdHandle = windll.kernel32.GetStdHandle
    windows_GetStdHandle.argtypes = [
        wintypes.DWORD
    ]
    windows_GetStdHandle.restype = wintypes.HANDLE

    def windows_stdout():
        return windows_GetStdHandle(stdout)

    windows_SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    windows_SetConsoleTextAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD
    ]
    windows_SetConsoleTextAttribute.restype = wintypes.BOOL

windows_fg = {
    "black": 0x0000,
    "red": 0x0004,
    "green": 0x0002,
    "blue": 0x0001
}

windows_fg["magenta"] = windows_fg["blue"] | windows_fg["red"]
windows_fg["yellow"] = windows_fg["red"] | windows_fg["green"]
windows_fg["cyan"] = windows_fg["green"] | windows_fg["blue"]
windows_fg["white"] = windows_fg["green"] | windows_fg["blue"] | windows_fg["red"]

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

windows_current_bg = windows_bg["black"]
windows_current_fg = windows_fg["white"]

windows_bold_fg = False
windows_bold_bg = False

windows_underline = False
windows_reverse = False

def do_windows_attrs():
    other = 0x0000
    if windows_bold_fg:
        other |= 0x0008
    if windows_bold_bg:
        other |= 0x0080
    if windows_underline:
        other |= 0x8000
    if windows_reverse:
        other |= 0x4000
    windows_SetConsoleTextAttribute(windows_stdout(), windows_current_fg | windows_current_bg | other)

nix_colors = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "reset": 0
}

def nix_color_code(code, bg=False, bold=False):
    print(f"\u001b[{code}{';' if bg else ''}{'1' if bold else ''}m", end="")

def reset():
    global windows_current_bg, windows_current_fg, windows_bold_bg, windows_bold_fg, windows_underline, windows_reverse
    if windows_mode:
        windows_current_bg = windows_bg["black"]
        windows_current_fg = windows_fg["white"]
        windows_bold_bg = False
        windows_bold_fg = False
        windows_underline = False
        windows_reverse = False
        do_windows_attrs()
    else:
        nix_color_code("00")

def underline():
    global windows_underline
    if windows_mode:
        windows_underline = True
        do_windows_attrs()
    else:
        print("\u001b[4m", end="")

def reverse():
    global windows_reverse
    if windows_mode:
        windows_reverse = True
        do_windows_attrs()
    else:
        print("\u001b[7m", end="")

def flush():
    sys.stdout.flush()

def console_color(color, bg=False, bold=False):
    global windows_current_fg, windows_current_bg, windows_bold_bg, windows_bold_fg
    if windows_mode:
        if bg == False:
            windows_current_fg = windows_fg[color]
        else:
            windows_current_bg = windows_bg[color]
        if bold:
            if bg:
                windows_bold_bg = True
            else:
                windows_bold_fg = True
        do_windows_attrs()
    else:
        nix_color_code(nix_colors[color], bg=bg, bold=bold)

def two_column(text1, text2, width):
    space_between = width - (len(text1) + len(text2))
    if space_between > -1:
        spacing = " " * space_between
        return text1 + spacing + text2

def constrain_text(text, width):
    lines = []
    amount_printed = 0
    total = len(text)
    while amount_printed < total:
        to_print = text[amount_printed:amount_printed+width]
        newline_pos = to_print.find("\n")
        if newline_pos != -1:
            to_print = text[amount_printed:amount_printed+newline_pos]
        lines.append(to_print)
        amount_printed += len(to_print) + (1 if newline_pos != -1 else 0)
    return lines

class Box:

    def __init__(self, width):
        self.width = width
        self.sections = []
        self.h_padding = 1 # Horizontal padding

    def inner_space(self):
        return self.width - 2 - (self.h_padding * 2)

    def add_section(self, text):
        self.sections.append(text)

    def render(self):
        padding = ' ' * self.h_padding
        separator = f"+{'-'*(self.width - 2)}+"
        for section in self.sections:
            print(separator)
            if type(section) == str:
                lines = constrain_text(section, self.inner_space())
                for line in lines:
                    print(two_column(f"|{padding}{line}", f"{padding}|", self.width))
            else:
                for line in section.compile():
                    print(f"|{padding}", end="")
                    section.render_line(line, end="")
                    print(f"{padding}|")
        print(separator)

"""