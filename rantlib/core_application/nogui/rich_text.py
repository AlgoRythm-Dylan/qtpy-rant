#from rantlib.core_application.nogui.util import *
from util import *

class Text:

    def __init__(self, text="", color="white", background="black"):
        self.text = text
        self.color = color
        self.background = background
        self.underlined = False
        self.reversed = False
        self.bold = False
        self.bright_background = False

class RichCharacter:

    def __init__(self, char, text_obj):
        self.character = char
        self.color = text_obj.color
        self.background = text_obj.background
        self.underlined = text_obj.underlined
        self.reversed = text_obj.reversed
        self.bold = text_obj.bold
        self.bright_background = text_obj.bright_background

    def has_same_formatting_as(self, other_char):
        return (self.color == other_char.color and
                self.background == other_char.background and
                self.underlined == other_char.underlined and
                self.reversed == other_char.reversed and
                self.bold == other_char.bold and
                self.bright_background == other_char.bright_background)

ALIGN_LEFT = "left"
ALIGN_CENTER = "center"
ALIGN_RIGHT = "right"

LEFT_TO_RIGHT = "ltr"
RIGHT_TO_LEFT = "rtl"

def is_word_breaker(character):
    character = ord(character)
    return not (
        (character >= ord('a') and character <= ord('z')) and
        (character >= ord('A') and character <= ord('Z')) and
        (character >= ord('0') and character <= ord('9')))

class RichText:

    def __init__(self):
        self.text = []
        self.total_lenth = 0
        self.max_width = None
        self.max_height = None
        self.min_width = None
        self.min_height = None
        self.alignment = ALIGN_LEFT
        self.writing_direction = LEFT_TO_RIGHT
        # If a word will be chopped into two lines, bump it to the next line.
        self.word_wrap = True
        # Break words longer than max_width into multiple lines
        self.word_break = True
        self.preserve_whitespace = False
        self.preserve_leading_whitespace = False

    def fixed_width(width):
        self.max_width = width
        self.min_width = width

    def fixed_height(height):
        self.max_height = height
        self.min_height = height

    def compile(self):
        # Shortcut if this object is empty
        if len(self.text) == 0:
            return []

        # Memory to render to
        lines = [[]]

        # State variables
        beginning_of_line = True
        last_character = None
        index = 0
        line_index = 0
        slice_index = 0
        text_index = 0
        characters_rendered = 0
        last_word_breaker = None

        while index < self.total_lenth:
            # The goal for this iteration is to get the next character to
            # render and its formatting and append it to the current line
            line = lines[line_index]
            slice = self.text[slice_index]
            # We need to find the next renderable character
            character = None
            while character == None:
                # Check if end of slice reached
                if text_index > len(slice.text) - 1:
                    slice_index += 1
                    text_index = 0
                    if slice_index < len(self.text):
                        # There's another slice to try
                        slice = self.text[slice_index]
                        continue
                    else:
                        # We are out of slices. Exit and return lines
                        return lines
                else:
                    character = slice.text[text_index]
                    text_index += 1
            # We now have a valid character and must determine whether or
            # not to display it
            if character == " ":
                if beginning_of_line:
                    if self.preserve_leading_whitespace:
                        line.append(RichCharacter(character, slice))
                else:
                    if self.preserve_whitespace or last_character != " ":
                        line.append(RichCharacter(character, slice))
                index += 1
            elif character == "\n" or (self.max_width != None and len(line) >= self.max_width):
                # End this line and create another
                line_index += 1
                lines.append([])
                beginning_of_line = True
                index += 1
            else:
                line.append(RichCharacter(character, slice))
                index += 1
            if beginning_of_line and character != " ":
                beginning_of_line = False
            last_character = character
        return lines # Just in case there was no text to render, reutrn empty list

    def render(self, compiled_text=None, reset_after=True, reset_after_line=False):
        if compiled_text == None:
            compiled_text = self.compile()
        for line in compiled_text:
            self.render_line(line, reset_after=reset_after_line)
        if reset_after:
            reset()

    def render_line(self, line, end="\n", reset_after=True):
        last_character = None
        for rich_character in line:
            if last_character == None or not last_character.has_same_formatting_as(rich_character):
                # Do formatting
                if not last_character == None:
                    flush() # Finalize color on Windows
                reset()
                console_color(rich_character.color, bold=rich_character.bold)
                console_color(rich_character.background, bg=True, bold=rich_character.bright_background)
                if rich_character.underlined:
                    underline()
                if rich_character.reversed:
                    reverse()
            print(rich_character.character, end="")
            last_character = rich_character
        flush()
        print(end, end="")
        if reset_after:
            reset()

    def add_text(self, text, reset_format=False):
        if reset_format or len(self.text) == 0:
            self.text.append(Text(text=text))
            self.total_lenth += len(text)
        elif type(text) == Text:
            self.text.append(text)
            self.total_lenth += len(text.text)
        else:
            last_text = self.text[len(self.text) - 1]
            last_text.text += text
            self.total_lenth += len(text)
            

if __name__ == "__main__":
    # Rendering test
    text = RichText()
    text.add_text("Hello\n")
    text.add_text(Text("world", color="blue"))
    text.render()