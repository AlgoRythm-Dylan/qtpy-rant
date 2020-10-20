# Generic class to hold a client since this application has both
# GUI and CLI mode, which may need to hold different data

class Client:

    def __init__(self, qtpy):
        self.qtpy = qtpy
        self.version = None

    def run(self):
        pass
