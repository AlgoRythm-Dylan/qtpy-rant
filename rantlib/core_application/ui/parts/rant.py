from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

class RantElement(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.rant = None
        self.upvote_button = QPushButton("++")
        self.score_label = QLabel()
        self.downvote_button = QPushButton("--")

    def set_rant(self, rant):
        self.rant = rant