class Event:

    def __init__(self):
        self.cancelled = False
        self.is_cancellable = True
        self.stopped = False

    def cancel(self):
        if not self.is_cancellable:
            raise Exception("Event is not cancellable")

    def stop(self):
        self.stopped = True

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
        if event_listeners == None:
            return
        for event_listener in event_listeners:
            try:
                event_listener.handle(event)
            except Exception as ex:
                print(ex)

    def on(self, event_name, handler):
        if not isinstance(handler, EventHandler) and callable(handler):
            # This is probably a simple function. Wrap it in a handler
            event_handler = EventHandler()
            event_handler.handle = handler
            handler = event_handler 
        is_new = not event_name in self.listeners.keys()
        if is_new:
            self.listeners[event_name] = [handler]
        else:
            self.listeners[event_name].append(handler)
        return handler # Since we may have created a handler from function

    def off(self, event_name, handler):
        events_list = self.listeners.get(event_name, [])
        try:
            events_list.remove(handler)
        except:
            pass
