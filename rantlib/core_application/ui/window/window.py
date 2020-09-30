from PyQt5.QtWidgets import QMainWindow
from rantlib.core_application.ui.theme import apply_theme

class Window(QMainWindow):

    def __init__(self, qtpy):
        super().__init__()
        self.qtpy = qtpy
        self.setObjectName("devrant_window")
        self.setMinimumSize(250, 150)
        self.resize(600, 450)

    def apply_theme(self):
        apply_theme(self)