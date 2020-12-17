from rantlib.app.gui.thread.worker import Worker
from rantlib.app.gui.theme import load_themes

class LoadThemesWorker(Worker):

    def __init__(self):
        self.themes = None

    def run(self):
        self.themes = load_themes()

    def finish(self):
        self.callback(self.themes)