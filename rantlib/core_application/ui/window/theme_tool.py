from rantlib.core_application.ui.window.window import Window
from rantlib.core_application.ui.theme import *
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QColor
from rantlib.core_application.ui.runnables.load_themes import LoadThemesRunnable

class ThemeTool(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle("qtpy-rant Theme Tool")
        self.setMinimumSize(650, 500)

        self.thread_pool = QThreadPool()
        self.ui = {} # Persistent UI stuff

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        palette = widget.palette()
        widget.setAutoFillBackground(True)
        palette.setColor(widget.backgroundRole(), QColor("#f7f7f7"))
        widget.setPalette(palette)

        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)
        layout.addWidget(sidebar)

        palette = sidebar.palette()
        sidebar.setAutoFillBackground(True)
        palette.setColor(sidebar.backgroundRole(), QColor("#e3e3e3"))
        sidebar.setPalette(palette)

        sidebar_label = QLabel()
        sidebar_label.setWordWrap(True)
        sidebar_label.setText("The Theme Tool is used to preview a theme and detect errors")
        sidebar_label.adjustSize()
        sidebar_layout.addWidget(sidebar_label)

        theme_area = QWidget()
        theme_area_layout = QVBoxLayout()
        theme_area.setLayout(theme_area_layout)
        layout.addWidget(theme_area, 1)

        select_theme_widget = QWidget()
        select_theme_layout = QHBoxLayout()
        select_theme_layout.setSpacing(0)
        select_theme_layout.setContentsMargins(0, 25, 0, 0)
        select_theme_widget.setLayout(select_theme_layout)

        select_theme_label = QLabel()
        select_theme_label.setText("Theme: ")
        select_theme_label.adjustSize()
        select_theme_layout.addWidget(select_theme_label)

        select_theme_combo = QComboBox()
        select_theme_combo.addItem("Loading...")
        select_theme_combo.setEnabled(False)
        select_theme_layout.addWidget(select_theme_combo, 1)
        self.ui["select_theme_combo"] = select_theme_combo

        sidebar_layout.addWidget(select_theme_widget)

        reload_theme_list_button = QLabel("Reload")
        reload_theme_list_button.setStyleSheet("QLabel {color: blue; margin-left: 5px; text-decoration: underline}")
        reload_theme_list_button.setCursor(Qt.PointingHandCursor)
        reload_theme_list_button.mousePressEvent = self.handle_list_reload_click
        select_theme_layout.addWidget(reload_theme_list_button)
        self.ui["reload_theme_list_button"] = reload_theme_list_button

        sidebar_layout.addStretch()

        self.spawn_theme_loader()

    def handle_list_reload_click(self, e):
        self.ui["reload_theme_list_button"].setDisabled(True)
        select_theme_combo = self.ui["select_theme_combo"]
        select_theme_combo.clear()
        select_theme_combo.addItem("Loading...")
        select_theme_combo.setEnabled(False)
        self.spawn_theme_loader()

    def spawn_theme_loader(self):
        self.thread_pool.start(LoadThemesRunnable(self.accept_theme_list))

    def accept_theme_list(self, theme_list):
        select_theme_combo = self.ui["select_theme_combo"]
        select_theme_combo.clear()
        for theme in theme_list:
            select_theme_combo.addItem(theme.title)
        select_theme_combo.setEnabled(True)
        self.ui["reload_theme_list_button"].setDisabled(False)