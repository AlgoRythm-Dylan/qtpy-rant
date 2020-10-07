class Config:

    def __init__(self):
        self.defaults = {}
        self.values = {}

    def set_default(self, key, value):
        self.defaults[key] = value

    def get(value, default=None):
        return self.values.get(value, default)

    def ensure_defaults(self):
        values_keys = self.values.keys()
        for key, value in self.defaults.items():
            if not key in values_keys:
                self.values[key] = value

    def data(self, data):
        for key, value in data.items():
            self.values[key] = value
        self.ensure_defaults()