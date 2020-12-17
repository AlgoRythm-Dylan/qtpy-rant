from PyQt5.QtCore import QThread

class Worker(QThread):
    
    def __init__(self, callback):
        QThread.__init__(self)
        self.callback = callback
        self.finished.connect(self.finish)

    def run(self):
        pass

    def finish(self):
        self.callback(self)
