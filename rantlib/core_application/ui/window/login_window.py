from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from rantlib.core_application.ui.window.window import Window
from rantlib.core_application.ui.parts.login_form import LoginForm
from rantlib.core_application.ui.theme import apply_theme

class LoginWindow(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle("Login to QtPy-Rant")
        self.setObjectName("devrant_window")
        self.setMinimumSize(450, 550)
        self.layout_widget = QWidget()
        self.layout_widget.setObjectName("devrant_secondary_panel")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout_widget.setLayout(layout)

        self.title_widget = QLabel(self.qtpy.language.get("service_name"))
        self.title_widget.setObjectName("devrant_title_label")
        layout.addWidget(self.title_widget, alignment=Qt.AlignHCenter)

        self.login_form = LoginForm(qtpy)
        self.login_form.setFixedWidth(400)
        layout.addWidget(self.login_form, alignment=Qt.AlignTop)

        self.setCentralWidget(self.layout_widget)
        apply_theme(qtpy.client, self.layout_widget)

        self.login_form.on("continue_as_guest", self.continue_as_guest)
        self.login_form.on("login", self.on_login)

    def continue_as_guest(self, ev):
        self.qtpy.client.spawn_main_window()
        self.close()

    def on_login(self, ev):
        if not ev.success:
            return
        self.qtpy.auth_service.add_user(ev.auth, set_current=True)
        self.qtpy.client.spawn_main_window()
        self.close()