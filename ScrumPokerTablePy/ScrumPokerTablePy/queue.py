from threading import Lock, Event


class EventQueue:
    def __init__(self):
        self.events = {}
        self.lock = Lock()

    def receive(self, event_name, timeout):
        self.lock.acquire(True)
        if event_name not in self.events:
            self.events[event_name] = Event()
        event = self.events[event_name]
        self.lock.release()
        return event.wait(timeout)

    def send(self, event_name):
        self.lock.acquire(True)
        if event_name in self.events:
            self.events[event_name].set()
            del self.events[event_name]
        self.lock.release()
