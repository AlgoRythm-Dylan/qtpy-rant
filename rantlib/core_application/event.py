class Event:

    def __init__(self):
        self.cancelled = False

class EventHandler:

    def __init__(self):
        self.enabled = True

    def handle(self, event):
        pass

class EventEmitter:
    
    def __init__(self):
        self.listeners = {}

    def dispatch(self, event_name, event):
        event_listeners = self.listeners.get(event_name)
        for event_listener in event_listeners:
            event_listener.handle(event)

    def on(self, event_name, handler):
        is_new = not event_name in self.listeners.keys()
        if is_new:
            self.listeners[event_name] = [handler]
        else:
            self.listeners[event_name].append(handler)

    def off(self, event_name, handler):
        events_list = self.listeners.get(event_name, [])
        try:
            events_list.remove(handler)
        except:
            pass
