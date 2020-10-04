from rantlib.core_application.ui.window.window import Window

class PagedWindow(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.page = None