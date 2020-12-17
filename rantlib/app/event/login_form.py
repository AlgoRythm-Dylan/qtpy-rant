from rantlib.app.event.event import Event

class LoginFormSubmitEvent(Event):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

class LoginEvent(Event):

    def __init__(self, success, auth):
        super().__init__()
        self.success = success
        self.auth = auth

class ContinueAsGuestEvent(Event):

    def __init__(self):
        super().__init__()