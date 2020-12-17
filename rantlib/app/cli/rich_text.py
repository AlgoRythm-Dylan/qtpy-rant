from rantlib.app.cli.util import *

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
    text_char = character
    character = ord(character)
    return not (
        (character >= ord('a') and character <= ord('z')) or
        (character >= ord('A') and character <= ord('Z')) or
        (character >= ord('0') and character <= ord('9')) or
        text_char in ('(', ')', '"', "%", '\'', '!', '?'))

class RichText:

    def __init__(self, raw_text=None):
        self.text = []
        self.total_length = 0
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

        if raw_text != None:
            self.add_text(raw_text)

    def fixed_width(self, width):
        self.max_width = width
        self.min_width = width

    def fixed_height(self, height):
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
        last_word_breaker = 0
        last_line_broken_explicitly = True # Did the last line end with a \n?

        while index < self.total_length:
            # The goal for this iteration is to get the next character to
            # render and its formatting and append it to the current line
            line = lines[line_index]
            beginning_of_line = len(line) == 0
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
            if character == "\n" or (self.max_width != None and len(line) >= self.max_width):
                # End this line and create another
                if character == "\n":
                    last_line_broken_explicitly = True
                else:
                    last_line_broken_explicitly = False
                index += 1
                lines.append([])
                line_index += 1
                if self.max_width != None and len(line) >= self.max_width and self.word_wrap:
                    # Manage word wrap
                    i = len(line) - 1
                    amount_to_reverse = 1
                    while i > 0 and not is_word_breaker(line[i].character):
                        line.pop(i)
                        amount_to_reverse += 1
                        i -= 1
                    index -= amount_to_reverse
                    i = amount_to_reverse
                    while i > 0:
                        if text_index == 0:
                            slice_index -= 1
                            slice = self.text[slice_index]
                            text_index = len(slice.text) - 1
                        text_index -= 1
                        i -= 1
                line = lines[line_index]
                beginning_of_line = True
            elif character == " ":
                if beginning_of_line:
                    if self.preserve_leading_whitespace and last_line_broken_explicitly:
                        line.append(RichCharacter(character, slice))
                else:
                    if self.preserve_whitespace or last_character != " ":
                        line.append(RichCharacter(character, slice))
                index += 1
            else:
                line.append(RichCharacter(character, slice))
                index += 1
            last_character = character
        return lines # Just in case there was no text to render, return empty list

    def render(self, compiled_text=None, reset_after=True, reset_after_line=False):
        if compiled_text == None:
            compiled_text = self.compile()
        for line in compiled_text:
            self.render_line(line, reset_after=reset_after_line)
        if reset_after:
            reset()
            flush()

    def render_line(self, line, end="\n", reset_after=True):
        last_character = None
        characters_rendered = 0
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
            characters_rendered += 1
        if self.min_width != None and characters_rendered < self.min_width:
            print(" " * (self.min_width - characters_rendered), end="")
        flush()
        print(end, end="")
        if reset_after:
            reset()
            flush()

    def add_text(self, text, reset_format=False):
        if type(text) == Text:
            self.text.append(text)
            self.total_length += len(text.text)
        else:
            if reset_format or len(self.text) == 0:
                self.text.append(Text(text=text))
                self.total_length += len(text)
            else:
                last_text = self.text[len(self.text) - 1]
                last_text.text += text
                self.total_length += len(text)
