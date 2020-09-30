from rantlib.core_application.ui.window.window import Window
from rantlib.core_application.ui.parts.header import Header
from PyQt5.QtWidgets import QBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle("devRant")

        self.header = Header()

        self.mainWidget = QWidget()
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.header)
        self.mainWidget.setLayout(layout)
        
        self.setCentralWidget(self.mainWidget)