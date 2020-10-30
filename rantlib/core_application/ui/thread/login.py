from rantlib.core_application.ui.thread.worker import Worker
from rantlib.core_application.event.event import Event
from rantlib.core_application.event.login_form import LoginEvent
from rantlib.devrant.devrant import login

class LoginWorker(Worker):

    def __init__(self, callback, username, password):
        super().__init__(callback)
        self.username = username
        self.password = password
        self.login_event = None

    def run(self):
        self.login_event = LoginEvent(False, None)
        try:
            auth = login(self.username, self.password)
            self.login_event.success = True
            self.login_event.auth = auth
        except:
            pass # Actually nothing to do here

    def finish(self):
        self.callback(self.login_event)