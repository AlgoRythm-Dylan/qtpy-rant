from PyQt5.QtCore import QRunnable

class CallbackRunnable(QRunnable):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def run(self):
        self.callback()