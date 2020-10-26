from rantlib.core_application.storage import write_data_file, read_data_file, STD_PATH_AUTH

class AuthService:

    def __init__(self):
        self.users = []
        self.current_session_key = None

    def read_data_file(self):
        data = read_data_file(STD_PATH_AUTH, default={})
        self.users = data.get("users", [])
        self.current_session_key = data.get("current_session_key")

    def current_user(self):
        if self.current_session_key == None:
            return None
        for user in users:
            if user.key == self.current_session_key:
                return user
        return None

    def add_user(self, user, set_current=False):
        self.users.add(user)
        if set_current:
            self.set_current_user(user)

    def set_current_user(self, user):
        self.current_session_key = user.key

    def write_data_file(self):
        write_data_file(STD_PATH_AUTH, self)