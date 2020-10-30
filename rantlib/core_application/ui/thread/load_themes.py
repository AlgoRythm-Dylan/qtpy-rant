from rantlib.core_application.ui.thread.worker import Worker
from rantlib.core_application.ui.theme import load_themes

class LoadThemesWorker(Worker):

    def __init__(self):
        self.themes = None

    def run(self):
        self.themes = load_themes()

    def finish(self):
        self.callback(self.themes)