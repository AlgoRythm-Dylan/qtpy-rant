from rantlib.core_application.config import Config

class TerminalConfig(Config):

    def __init__(self):
        super().__init__()
        self.set_default("prompt", "[green_fg][user] [reset]>> ")
        self.set_default("preferred_width", 80)
        self.set_default("preference_colors_enabled", False)
        self.set_default("blank_command_repeats_last", False)