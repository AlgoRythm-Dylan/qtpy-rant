from rantlib.core_application.config import Config

class TerminalConfig(Config):

    def __init__(self):
        super().__init__()
        self.set_default("prompt", "\\u >> ")