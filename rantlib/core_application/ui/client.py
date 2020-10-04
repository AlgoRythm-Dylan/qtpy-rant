import sys
from pathlib import Path
from rantlib.core_application.client import Client
from rantlib.core_application.ui.window.mainwindow import MainWindow
from rantlib.core_application.ui.window.theme_tool import ThemeTool

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
except ImportError as e:
    print("[qtpy-rant]: Could not import packages (Are they installed?)", file=sys.stderr)
    print(ex, file=sys.stderr)
    sys.exit(1)

class QtClient(Client):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.qapplication = QApplication(sys.argv)
        self.windows = []
        res_path = Path(__file__).parent.parent.parent.parent.joinpath("res")
        comfortaa_id = QFontDatabase.addApplicationFont(str(res_path.joinpath("Comfortaa-Regular.ttf")))
        self.comfortaa_font_family = QFontDatabase.applicationFontFamilies(comfortaa_id)[0]
        roboto_id = QFontDatabase.addApplicationFont(str(res_path.joinpath("Roboto-Regular.ttf")))
        self.roboto_font_family = QFontDatabase.applicationFontFamilies(roboto_id)[0]
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