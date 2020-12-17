from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QThreadPool

from rantlib.app.event.event import EventEmitter
from rantlib.app.gui.thread.login import LoginWorker
from rantlib.app.event.login_form import *

class LoginForm(QWidget, EventEmitter):

    def __init__(self, qtpy, include_warning=True):
        QWidget.__init__(self)
        EventEmitter.__init__(self)
        self.qtpy = qtpy
        self.thread_pool = QThreadPool()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("devrant_input")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setObjectName("devrant_input")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.submit_button = QPushButton("Submit")
        self.submit_button.setObjectName("devrant_button")
        self.submit_button.setDefault(True)
        self.error_message = QLabel()
        self.error_message.setWordWrap(True)
        self.error_message.setAlignment(Qt.AlignCenter)
        self.error_message.hide()
        self.error_message.setObjectName("devrant_error_label")
        self.continue_as_guest_link = QLabel("Continue as Guest")
        self.continue_as_guest_link.setObjectName("devrant_link_label")
        self.continue_as_guest_link.setAlignment(Qt.AlignHCenter)
        self.continue_as_guest_link.mousePressEvent = self.handle_continue_as_guest

        self.submit_button.pressed.connect(self.handle_submit)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(self.username_input, alignment=Qt.AlignTop)
        layout.addWidget(self.password_input, alignment=Qt.AlignTop)
        layout.addWidget(self.error_message, alignment=Qt.AlignTop)
        layout.addWidget(self.submit_button, alignment=Qt.AlignTop)
        layout.addWidget(self.continue_as_guest_link, alignment=Qt.AlignTop)

        if include_warning:
            self.warning_label = QLabel(self.qtpy.language.get("third_party_warning"))
            self.warning_label.setWordWrap(True)
            self.warning_label.setObjectName("devrant_alt_label")
            self.warning_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.warning_label, alignment=Qt.AlignTop)

        #layout.addStretch()
        self.setLayout(layout)

    def handle_submit(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if len(username) == 0:
            self.display_error("Username is required")
            return
        elif len(password) == 0:
            self.display_error("Password is required")
            return
        event = LoginFormSubmitEvent(username, password)
        self.dispatch("submit", event)
        if not event.cancelled:
            self.disable(True)
            self.worker = LoginWorker(self.on_login_response, event.username, event.password)
            self.worker.start()

    def handle_continue_as_guest(self, e):
        self.dispatch("continue_as_guest", ContinueAsGuestEvent())

    def disable(self, disabled):
        self.username_input.setDisabled(disabled)
        self.password_input.setDisabled(disabled)
        self.submit_button.setDisabled(disabled)

    def on_login_response(self, login_event):
        self.disable(False)
        if not login_event.success:
            self.display_error(self.qtpy.language.get("login_failure"))
        self.dispatch("login", login_event)

    def display_error(self, message):
        self.error_message.setText(message)
        self.error_message.show()