"""
Event definitions and interfaces ---
used for Model-View-Controller user
interface but also for other coordination
based on event notification.

In this variation on listeners, we use a subclass
for each event type. This gives us a flexible way to
add specific information for different kinds of
events, if we need to.
"""

# ------------
#  The events
# ------------


class Event(object):
    """Abstract base class of all events, both for MVC
    and for other purposes.
    """
    pass


# class BoardEvent(Event):
#     """Abstract base class for things that happen
#     to the Sudoku board as a whole.
#     """
#     def __init__(self, grid: board.Board):
#         self.grid = grid

# Concrete events.  For many of these, the only additional
# information is the class itself.


# class TileCreated(BoardEvent):
#     pass

# ---------------
# Listeners
# ---------------

class Listener(object):
    """Abstract base class for listeners.
    Subclass this to make the notification do
    something useful.
    """

    def __init__(self):
        """Default constructor for simple listeners without state"""
        pass

    def notify(self, event: Event):
        """The 'notify' method of the base class must be
        overridden in concrete classes.
        """
        raise NotImplementedError("You must override Listener.notify")
