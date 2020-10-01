import sys
from rantlib.core_application.client import Client
from rantlib.core_application.ui.window.mainwindow import MainWindow
from rantlib.core_application.ui.window.theme_tool import ThemeTool

try:
    from PyQt5.QtWidgets import QApplication
except ImportError as e:
    print("[qtpy-rant]: Could not import packages (Are they installed?)", file=sys.stderr)
    print(ex, file=sys.stderr)
    sys.exit(1)

class QtClient(Client):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.qapplication = QApplication(sys.argv)
        self.windows = []
        if qtpy.args.theme_tool:
            main_window = ThemeTool(qtpy)
            self.windows.append(main_window)
            self.main_window = main_window
        else:
            main_window = MainWindow(qtpy)
            self.windows.append(main_window)
            self.main_window = main_window

    def run(self):
        self.main_window.show()
        self.qapplication.exec_()