from rantlib.app.storage import read_data_file, write_data_file

# Base config class
class Config:

    def __init__(self):
        self.defaults = {}
        self.values = {}

    def set_default(self, key, value):
        self.defaults[key] = value

    def get(self, value, default=None):
        return self.values.get(value, default)

    def set(self, key, value):
        self.values[key] = value

    def remove(self, key):
        del self.values[key]

    def has_default(self, key):
        return key in self.defaults.keys()

    def restore_default(self, key):
        if not self.has_default(key):
            raise Exception("Key does not have a default")
        else:
            self.values[key] = self.defaults[key]

    def ensure_defaults(self):
        values_keys = self.values.keys()
        for key, value in self.defaults.items():
            if not key in values_keys:
                self.values[key] = value

    def data(self, data):
        for key, value in data.items():
            self.values[key] = value
        self.ensure_defaults()

    def read_data_file(self, path):
        self.data(read_data_file(path, default={}))

    def write_data_file(self, path):
        write_data_file(path, self.values)

# Application config class
class QtPyRantConfig(Config):

    def __init__(self):
        super().__init__()
        self.set_default("language", "EN-US")