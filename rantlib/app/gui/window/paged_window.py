from rantlib.app.gui.window.window import Window

class PagedWindow(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.page = None