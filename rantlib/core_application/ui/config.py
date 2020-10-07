from rantlib.core_application.config import Config

class UIConfig(Config):

    def __init__(self):
        super().__init__()
        self.set_default("theme_file", "default.json")