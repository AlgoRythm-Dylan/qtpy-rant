from rantlib.core_application.storage import write_data_file, read_data_file, STD_PATH_AUTH

class AuthService:

    def __init__(self):
        self.users = []

    def load_auth_items(self):
        data = read_data_file(STD_PATH_AUTH, default={})
        self.users = data.get("users", [])

    def save_auth_items(self):
        write_data_file(STD_PATH_AUTH, self)