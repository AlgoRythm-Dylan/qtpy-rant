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
<<<<<<< HEAD
            if auth.key == self.current_session_key:
=======
            if user.key == self.current_session_key:
>>>>>>> 72ba524da1d23081747ae9c80d845840e9714d8b
                return user
        return None

    def add_user(self, user, set_current=False):
        self.users.add(user)
        if set_current:
            self.set_current_user(user)

    def set_current_user(self, user):
<<<<<<< HEAD
        self.current_session_key = auth.key
=======
        self.current_session_key = user.key
>>>>>>> 72ba524da1d23081747ae9c80d845840e9714d8b

    def write_data_file(self):
        write_data_file(STD_PATH_AUTH, self)