from rantlib.app.gui.thread.rants import RantWorker
from rantlib.app.event.event import EventEmitter
from rantlib.devrant.devrant import RantLib

class RantGetter(EventEmitter):

    def __init__(self):
        super().__init__()
        self.skip = 0
        self.stride = 50
        self.sort = "algo" # algo, top, recent
        self.time_range = "day" # day, week, month, all
        self.token_id = None
        self.token_key = None
        self.user_id = None
        self.worker = None

    def get(self, amount=None, mode=None):
        if amount == None:
            amount = self.stride
        if mode == None:
            mode = self.sort
        rants = RantLib.rant_feed(mode=mode,time_range=self.time_range,
                                  limit=amount,skip=self.skip,token_id=self.token_id,
                                  token_key=self.token_key,user_id=self.user_id)
        self.skip += amount
        return rants

    def get_in_worker(self, amount=None, mode=None):
        if amount == None:
            amount = self.stride
        if mode == None:
            mode = self.sort
        if not self.worker == None:
            self.worker = RantWorker(mode=mode)

    def accept_worker_data(self, rants):
        pass