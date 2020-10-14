from PyQt5.QtWidgets import QWidget, QLabel, QBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class Header(QWidget):

    def __init__(self, qtpy):
        super().__init__()
        self.qtpy = qtpy

        self.setObjectName("devrant_secondary_panel")
        self.setFixedHeight(60)

        self.label = QLabel()
        self.label.setObjectName("devrant_title_label")
        self.label.setText(self.qtpy.language.get("service_name"))

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
