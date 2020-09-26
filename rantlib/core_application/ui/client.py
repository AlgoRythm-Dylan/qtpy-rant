from rantlib.core_application.client import Client

class QtClient(Client):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.qapplication = None
        self.main_window = None

    def run(self):
        self.qapplication.exec_()