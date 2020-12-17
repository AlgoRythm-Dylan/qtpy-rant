from rantlib.app.storage import write_data_file, read_data_file, STD_PATH_AUTH
from rantlib.devrant.devrant import Auth

class AuthService:

    def __init__(self):
        self.users = []
        self.current_session_key = None

    def read_data_file(self):
        data = read_data_file(STD_PATH_AUTH, default={})
        users = data.get("users", [])
        for user in users:
            auth = Auth()
            auth.import_data(user)
            self.users.append(auth)
        self.current_session_key = data.get("current_session_key")

    def current_user(self):
        if self.current_session_key == None:
            return None
        for user in self.users:
            if user.key == self.current_session_key:
                return user
        return None

    def add_user(self, user, set_current=False, write_file=True):
        self.users.append(user)
        if set_current:
            self.set_current_user(user)
        self.write_data_file()

    def set_current_user(self, user):
        self.current_session_key = user.key

    def write_data_file(self):
        write_data_file(STD_PATH_AUTH, self)