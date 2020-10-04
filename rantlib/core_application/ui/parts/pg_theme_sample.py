from rantlib.core_application.ui.parts.page import Page
from rantlib.core_application.ui.theme import apply_theme_to_widget
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ThemeSamplePage(Page):

    def __init__(self, qtpy):
        super().__init__()
        self.themed_items = []
        self.labels = []
        self.qtpy = qtpy

        theme_area_widget = QWidget()
        theme_area_widget_layout = QVBoxLayout()
        theme_area_widget.setLayout(theme_area_widget_layout)
        theme_area_widget.setObjectName("theme_area_widget")
        theme_area_widget.setStyleSheet("QWidget { background-color: white; color: black; }")
        self.root = theme_area_widget

        theme_area_widget_layout.addWidget(QLabel("devrant_window"), alignment=Qt.AlignTop)
        window_widget = QWidget()
        self.labels.append(QLabel("text", parent=window_widget))
        window_widget.setObjectName("devrant_window")
        window_widget.setFixedHeight(30)
        theme_area_widget_layout.addWidget(window_widget, 1)
        self.themed_items.append(window_widget)

        theme_area_widget_layout.addWidget(QLabel("devrant_panel"), alignment=Qt.AlignTop)
        devrant_panel_widget = QWidget()
        self.labels.append(QLabel("text", parent=devrant_panel_widget))
        devrant_panel_widget.setObjectName("devrant_panel")
        devrant_panel_widget.setFixedHeight(30)
        theme_area_widget_layout.addWidget(devrant_panel_widget, 1)
        self.themed_items.append(devrant_panel_widget)

        theme_area_widget_layout.addWidget(QLabel("devrant_secondary_panel"), alignment=Qt.AlignTop)
        devrant_secondary_panel_widget = QWidget()
        self.labels.append(QLabel("text", parent=devrant_secondary_panel_widget))
        devrant_secondary_panel_widget.setObjectName("devrant_secondary_panel")
        devrant_secondary_panel_widget.setFixedHeight(30)
        theme_area_widget_layout.addWidget(devrant_secondary_panel_widget, 1)
        self.themed_items.append(devrant_secondary_panel_widget)

        theme_area_widget_layout.addWidget(QLabel("devrant_alt_label"), alignment=Qt.AlignTop)
        devrant_alt_label_widget = QWidget()
        self.labels.append(QLabel("text", parent=devrant_alt_label_widget))
        devrant_alt_label_widget.setObjectName("devrant_alt_label")
        devrant_alt_label_widget.setFixedHeight(30)
        theme_area_widget_layout.addWidget(devrant_alt_label_widget, 1)
        self.themed_items.append(devrant_alt_label_widget)

        theme_area_widget_layout.addWidget(QLabel("devrant_button"), alignment=Qt.AlignTop)
        devrant_button_widget = QPushButton("text")
        devrant_button_widget.setObjectName("devrant_button")
        theme_area_widget_layout.addWidget(devrant_button_widget, 1)
        self.themed_items.append(devrant_button_widget)

        theme_area_widget_layout.addWidget(QLabel("devrant_vote_button"), alignment=Qt.AlignTop)
        devrant_vote_button_widget = QPushButton("++")
        devrant_vote_button_widget.setObjectName("devrant_vote_button")
        theme_area_widget_layout.addWidget(devrant_vote_button_widget, 1)
        self.themed_items.append(devrant_vote_button_widget)
        theme_area_widget_layout.addStretch()

    def apply_theme(self, theme):
        for theme_item in self.themed_items:
            apply_theme_to_widget(self.qtpy.client, theme_item, theme)
        for label in self.labels:
            label.adjustSize()