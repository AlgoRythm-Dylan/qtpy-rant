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
        rendered = ""
        padding = ' ' * self.h_padding
        separator = f"+{'-'*(self.width - 2)}+\n"
        for section in self.sections:
            rendered += separator
            lines = constrain_text(section, self.inner_space())
            for line in lines:
                rendered += two_column(f"|{padding}{line}", f"{padding}|", self.width) + "\n"
        rendered += separator
        return rendered