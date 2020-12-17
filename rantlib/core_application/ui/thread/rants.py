from rantlib.core_application.ui.thread.worker import Worker
from rantlib.devrant.devrant import RantLib

class RantWorker(Worker):

    def __init__(self, callback, mode="algo", time_range="day", limit=50, skip=0, token_id=None, token_key=None, user_id=None):
        super().__init__(callback)
        self.rants = None

        self.mode = mode
        self.time_range = time_range
        self.limit = limit
        self.skip = skip
        self.token_id = token_id
        self.token_key = token_key
        self.user_id = user_id

    def run(self):
        self.rants = RantLib.rant_feed(mode=self.mode, time_range=self.time_range,
                                       limit=self.limit, skip=self.skip, token_id=self.token_id,
                                       token_key=self.token_key, user_id=self.user_id)

    def finish(self):
        self.callback(self.rants)