from rantlib.core_application.ui.runnables.callback import CallbackRunnable
from rantlib.core_application.event.event import Event
from rantlib.core_application.event.login_form import LoginEvent
from rantlib.devrant.devrant import login

class LoginRunnable(CallbackRunnable):

    def __init__(self, callback, username, password):
        super().__init__(callback)
        self.username = username
        self.password = password

    def run(self):
        login_event = LoginEvent(False, None)
        try:
            auth = login(self.username, self.password)
            login_event.success = True
            login_event.auth = auth
        except:
            pass # Actually nothing to do here
        self.callback(login_event)