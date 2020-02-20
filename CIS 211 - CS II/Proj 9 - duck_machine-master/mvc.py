"""
Base components for connecting model to view.
"""

class MVCEvent(object):
    """Abstract base class for events"""

    def __init__(self, subject: any) -> None:
        """The 'subject' is the object announcing the event"""
        self.subject = subject


class MVCListener(object):
    """Abstract base class.
    Extend this and override the notify method.
    """

    def notify(self, MVCEvent) -> None:
        """Override this method in listeners"""
        raise NotImplementedError("The notify method should be overridden in {}".format(self.__class__))

class MVCListenable(object):
    """A model object that a view object can listen to"""

    def __init__(self):
        self.listeners = [ ]

    def register_listener(self, listener: MVCListener) -> None:
        self.listeners.append(listener)

    def notify_all(self, event: MVCEvent) -> None:
        for listener in self.listeners:
            listener.notify(event)

