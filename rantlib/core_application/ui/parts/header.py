from PyQt5.QtWidgets import QWidget, QLabel, QBoxLayout
from PyQt5.QtGui import QColor

class Header(QWidget):

    def __init__(self):
        super().__init__()

        palette = self.palette()
        self.setAutoFillBackground(True)
        palette.setColor(self.backgroundRole(), QColor("#40415a"))
        self.setPalette(palette)

        self.setFixedHeight(60)

        self.label = QLabel()
        self.label.setText("devRant")

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addWidget(self.label)
        self.setLayout(layout)
