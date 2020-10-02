from rantlib.core_application.ui.runnables.callback import CallbackRunnable
from rantlib.core_application.ui.theme import load_themes

class LoadThemesRunnable(CallbackRunnable):

    def run(self):
        self.callback(load_themes())