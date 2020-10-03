from rantlib.core_application.ui.window.window import Window
from rantlib.core_application.ui.theme import *
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QColor
from rantlib.core_application.ui.runnables.load_themes import LoadThemesRunnable

class ThemeTool(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle("qtpy-rant Theme Tool")
        self.setMinimumSize(550, 450)

        self.thread_pool = QThreadPool()

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        sidebar = QWidget(widget)
        sidebar.setMaximumWidth(250)
        sidebar.setFixedWidth(250)

        sidebar.setLayout(QHBoxLayout())
        sidebar.layout().setContentsMargins(0, 0, 0, 0)
        layout.addWidget(sidebar, 1)

        sidebar_scroller = QScrollArea()
        sidebar.layout().addWidget(sidebar_scroller, 1)
        sidebar_scroller.setWidgetResizable(True)
        sidebar_scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        sidebar_widget = QWidget()
        sidebar_scroller.setWidget(sidebar_widget)
        sidebar_widget_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_widget_layout)

        sidebar_widget.setStyleSheet("QWidget { background-color: #ededed; color: black; }")

        sidebar_label = QLabel()
        sidebar_label.setWordWrap(True)
        sidebar_label.setText("The Theme Tool is used to preview a theme and detect errors")
        sidebar_label.adjustSize()
        sidebar_widget_layout.addWidget(sidebar_label, alignment=Qt.AlignTop)

        theme_area = QWidget()
        theme_area_layout = QVBoxLayout()
        theme_area_layout.setContentsMargins(0, 0, 0, 0)
        theme_area.setLayout(theme_area_layout)
        layout.addWidget(theme_area, 1)
        theme_area.setStyleSheet("QWidget { background-color: #f7f7f7; color: black; }")

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
        self.select_theme_combo = select_theme_combo

        sidebar_widget_layout.addWidget(select_theme_widget, alignment=Qt.AlignTop)

        reload_theme_list_button = QLabel("Reload")
        reload_theme_list_button.setStyleSheet("QLabel {color: blue; margin-left: 5px; text-decoration: underline}")
        reload_theme_list_button.setCursor(Qt.PointingHandCursor)
        reload_theme_list_button.mousePressEvent = self.handle_list_reload_click
        select_theme_layout.addWidget(reload_theme_list_button)
        self.reload_theme_list_button = reload_theme_list_button

        sidebar_widget_layout.addStretch()

        theme_area_scroller = QScrollArea()
        theme_area_layout.addWidget(theme_area_scroller, 1)
        theme_area_scroller.setWidgetResizable(True)

        theme_area_widget = QWidget()
        theme_area_scroller.setWidget(theme_area_widget)
        theme_area_widget_layout = QVBoxLayout()
        theme_area_widget.setLayout(theme_area_widget_layout)

        self.spawn_theme_loader()

    def handle_list_reload_click(self, e):
        self.reload_theme_list_button.setDisabled(True)
        select_theme_combo = self.select_theme_combo
        select_theme_combo.clear()
        select_theme_combo.addItem("Loading...")
        select_theme_combo.setEnabled(False)
        self.spawn_theme_loader()

    def spawn_theme_loader(self):
        self.thread_pool.start(LoadThemesRunnable(self.accept_theme_list))

    def accept_theme_list(self, theme_list):
        select_theme_combo = self.select_theme_combo
        select_theme_combo.clear()
        for theme in theme_list:
            select_theme_combo.addItem(theme.title)
        select_theme_combo.setEnabled(True)
        self.reload_theme_list_button.setDisabled(False)