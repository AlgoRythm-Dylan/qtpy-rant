from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from rantlib.core_application.ui.theme import apply_theme
from pathlib import Path

class Window(QMainWindow):

    def __init__(self, qtpy):
        super().__init__()
        self.qtpy = qtpy
        self.setMinimumSize(250, 150)
        self.resize(600, 450)
        stylesheet = open(Path(__file__).parent.parent.parent.parent.parent.joinpath("res/app.qss"))
        self.setStyleSheet(stylesheet.read())
        stylesheet.close()
        icon_path = Path(__file__).parent.parent.parent.parent.parent.joinpath("res/favicon16.png")
        self.setWindowIcon(QIcon(str(icon_path)))

    def apply_theme(self):
        apply_theme(self)