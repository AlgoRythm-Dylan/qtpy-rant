from PyQt5.QtWidgets import QMainWindow

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 150)
        self.resize(600, 450)