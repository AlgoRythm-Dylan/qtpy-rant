from PyQt5.QtCore import Qt

class WindowState:
    
    def __init__(self):
        self.position = (10, 10)
        self.size = (600, 450)
        self.is_maximized = False

    def record_state(self, window):
        self.is_maximized = bool(window.windowState() & Qt.WindowMaximized)
        if not self.is_maximized:
            self.size = (window.geometry().width(), window.geometry().height())
            self.position = (window.x(), window.y())

    def data(self, data):
        self.position = tuple(data.get("position", self.position))
        self.size = tuple(data.get("size", self.size))
        self.is_maximized = data.get("is_maximized", self.is_maximized)