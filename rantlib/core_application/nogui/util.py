def print_two_column(text1, text2, width):
    space_between = width - (len(text1) + len(text2))
    if space_between > 0:
        spacing = " " * space_between
        print(text1 + space_between + text2)

class Box:

    def __init__(self, width):
        self.width = width
        self.sections = []
        self.h_padding = 1 # Horizontal padding

    def add_section(self, text):
        self.sections.add(text)

    def render(self):
        for section in self.sections:
            pass