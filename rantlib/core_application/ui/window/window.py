from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from rantlib.core_application.ui.theme import apply_theme
from rantlib.core_application.storage import read_window_state, write_window_state
from rantlib.core_application.ui.window.window_state import WindowState
from pathlib import Path


class Window(QMainWindow):

    def __init__(self, qtpy):
        super().__init__()
        self.qtpy = qtpy
        self.setMinimumSize(250, 150)
        stylesheet = open(Path(__file__).parent.parent.parent.parent.parent.joinpath("res/app.qss"))
        self.setStyleSheet(stylesheet.read())
        stylesheet.close()
        icon_path = Path(__file__).parent.parent.parent.parent.parent.joinpath("res/favicon16.png")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.window_state = read_window_state(type(self).__name__)
        self.restore_to_state()

    def apply_theme(self):
        apply_theme(self)

    def record_state(self):
        self.window_state.record_state(self)
        write_window_state(type(self).__name__, self.window_state)

    def restore_to_state(self):
        self.resize(self.window_state.size[0], self.window_state.size[1])
        self.move(self.window_state.position[0], self.window_state.position[1])
        if self.window_state.is_maximized:
            self.setWindowState(Qt.WindowMaximized)

    def closeEvent(self, event):
        self.record_state()