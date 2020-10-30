import sys
from pathlib import Path
from rantlib.core_application.client import Client
from rantlib.core_application.ui.window.main_window import MainWindow
from rantlib.core_application.ui.window.login_window import LoginWindow
from rantlib.core_application.ui.window.theme_tool import ThemeTool
from rantlib.core_application.ui.theme import load_theme
from rantlib.core_application.storage import read_data_file, STD_PATH_GUI_CONFIG
from rantlib.core_application.ui.config import UIConfig

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
        self.version = "0.1.0"
        self.qapplication = QApplication(sys.argv)
        self.windows = []
        res_path = Path(__file__).parent.parent.parent.parent.joinpath("res")
        comfortaa_id = QFontDatabase.addApplicationFont(str(res_path.joinpath("Comfortaa-Regular.ttf")))
        self.comfortaa_font_family = QFontDatabase.applicationFontFamilies(comfortaa_id)[0]
        roboto_id = QFontDatabase.addApplicationFont(str(res_path.joinpath("Roboto-Regular.ttf")))
        self.roboto_font_family = QFontDatabase.applicationFontFamilies(roboto_id)[0]
        self.config = UIConfig()
        self.config.read_data_file(STD_PATH_GUI_CONFIG)
        self.theme = load_theme(self.config.get("theme_file"))

    def run(self):
        if self.qtpy.args.theme_tool:
            main_window = ThemeTool(self.qtpy)
            self.windows.append(main_window)
            self.main_window = main_window
        else:
            if len(self.qtpy.auth_service.users) == 0:
                login_window = LoginWindow(self.qtpy)
                self.windows.append(login_window)
                self.main_window = login_window
            else:
                main_window = MainWindow(self.qtpy)
                self.windows.append(main_window)
                self.main_window = main_window
        self.main_window.show()
        self.qapplication.exec_()