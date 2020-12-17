from rantlib.app.event.event import Event

class RantsLoadedEvent(Event):

    def __init__(self, rants):
        super().__init__()
        self.rants = rants