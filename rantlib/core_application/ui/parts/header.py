from PyQt5.QtWidgets import QWidget, QLabel, QBoxLayout
from PyQt5.QtGui import QColor

class Header(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("devrant_secondary_panel")
        self.setFixedHeight(60)

        self.label = QLabel()
        self.label.setText("devRant")
        self.label.setStyleSheet("* { font-family: Comfortaa; font-size: 30px; }")

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addWidget(self.label)
        self.setLayout(layout)
