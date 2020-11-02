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
        self.alignment = "left"
        self.preserve_whitespace = False

    def has_more_lines(self, progress):
        pass

    def start_render(self):
        progress = RenderProgress()
        return progress

    def render(self, progress):
        while self.has_more_lines(progress):
            self.render(progress)
        return progress

    def render_line(self, progress):
        characters_to_render = self.total_lenth - progress.text_index
        if self.max_width != None and characters_to_render > self.max_width:
            characters_to_render = self.max_width
        characters_rendered = 0
        beginning_of_line = True
        while characters_rendered < characters_to_render:
            character =             
            characters_rendered += 1

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