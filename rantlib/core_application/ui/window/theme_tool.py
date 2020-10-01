from rantlib.core_application.ui.window.window import Window
from rantlib.core_application.ui.theme import *

class ThemeTool(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle("qtpy-rant Theme Tool")
