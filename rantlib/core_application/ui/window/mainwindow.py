from rantlib.core_application.ui.window.window import Window
from rantlib.core_application.ui.parts.header import Header
from rantlib.core_application.ui.theme import apply_theme
from PyQt5.QtWidgets import QBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle(qtpy.language.get("app_name"))

        self.header = Header(qtpy)

        self.main_widget = QWidget()
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.header)
        self.main_widget.setLayout(layout)
        
        self.setCentralWidget(self.main_widget)

        apply_theme(self.qtpy.client, self.main_widget)