#from rantlib.core_application.nogui.util import *
from util import *

class Text:

    def __init__(self, text=""):
        self.text = text
        self.color = None # Default color
        self.background = None # Default background

class RenderProgress:

    def __init__(self):
        self.text_object_index = 0
        self.text_object_interior_index = 0
        self.text_index = 0
        self.line = 0

class RichText:

    def __init__(self):
        self.text = []
        self.total_lenth = 0
        self.max_width = None
        self.max_height = None
        self.min_width = None
        self.min_height = None
        self.alignment = "left"
        self.preserve_whitespace = False

    def fixed_width(width):
        self.max_width = width
        self.min_width = width

    def fixed_height(height):
        self.max_height = height
        self.min_height = height

    def has_more_lines(self, progress):
        on_last_slice = progress.text_object_index >= len(self.text) - 1
        last_slice_text_length = len(self.text[len(self.text) - 1].text)
        at_end_of_last_slice = progress.text_object_interior_index >= last_slice_text_length - 1
        return not (on_last_slice and at_end_of_last_slice)

    def start_render(self):
        progress = RenderProgress()
        return progress

    def render(self, progress):
        while self.has_more_lines(progress):
            self.render_line(progress)
        return progress

    def render_line(self, progress, end=None):
        characters_to_render = self.total_lenth - progress.text_index
        if self.max_width != None and characters_to_render > self.max_width:
            characters_to_render = self.max_width
        characters_rendered = 0
        beginning_of_line = True
        last_character = None
        current_slice = self.text[progress.text_object_index]
        while characters_rendered < characters_to_render:
            # Make sure index is within bounds of current slice
            if progress.text_object_interior_index > len(current_slice.text) - 1:
                has_next_slice = not progress.text_object_index > len(self.text) - 1
                if has_next_slice:
                    progress.text_object_index += 1
                    progress.text_object_interior_index = 0
                    current_slice = self.text[progress.text_object_index]
                else:
                    break
            character = current_slice.text[progress.text_object_interior_index]
            print(character, end="")
            last_character = character
            progress.text_object_interior_index += 1
            characters_rendered += 1
        if end != None and end != "":
            print(end, end="")

    def add_text(self, text, reset_format=False):
        if reset_format or len(self.text) == 0:
            self.text.append(Text(text=text))
        else:
            last_text = self.text[len(self.text) - 1]
            last_text.text += text
        self.total_lenth += len(text)
            

if __name__ == "__main__":
    # Rendering test
    text = RichText()
    progress = text.start_render()
    text.add_text("Hello", reset_format=True)
    text.add_text(" world", reset_format=True)
    text.render(progress)