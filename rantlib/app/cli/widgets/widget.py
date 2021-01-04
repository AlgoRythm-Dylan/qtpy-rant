from qtpyr.cli import Box, WidgetStyle

class Widget(Box):

    def __init__(self):
        super().__init__()
        self.name = ""
        self.parent = None
        self.children = []
        self.style = WidgetStyle()

    def render(self, box):
        pass
