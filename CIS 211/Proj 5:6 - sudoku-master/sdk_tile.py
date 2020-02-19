"""
Sudoku Tile objects hold both a current
value and constraints on possible values.
Each tile may belong to more than one group
(nonet), and be constrained by selected values
of other tiles in any of its groups.
"""
import typing
from typing import Set, Sequence

# MVC listener interface definition
from events import Event, Listener

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Some globals that could be used to customize the
# board, e.g., using symbols other than '0'..'9' for
# tiles.
CHOICES = ['1', '2', '3', '4', '5',
           '6', '7', '8', '9']
UNKNOWN = '.'

# -------------------------------
# Interface for listeners
#  (Notes on design decision at end of this file)
# -------------------------------


class TileEvent(Event):
    """Abstract base class for things that happen
    to tiles. We always indicate the tile.  Concrete
    subclasses indicate the nature of the event.
    """

    def __init__(self, tile: 'Tile'):
        self.tile = tile
        # Note 'Tile' type is a forward reference;

    def __str__(self):
        """Printed representation includes name of concrete subclass"""
        return "{}[{},{}]:{}/{}".format(
            type(self).__name__, self.row, self.col,
            self.value, self.candidates)

# A subclass for each kind of event


class TileChanged(TileEvent):
    """Something has changed, either value or candidates"""
    pass


class TileGuessed(TileEvent):
    """This value change is a guess by the back-track solver"""
    pass


class TileAttend(TileEvent):
    """This tile currently participating in constraint propagation"""
    pass


class TileUnattend(TileEvent):
    """Done with this tile for now"""
    pass


class TileListener(Listener):
    def notify(self, event: TileEvent):
        raise NotImplementedError(
            "TileListener subclass needs to override notify(TileEvent)")

# ------------------------------
#  Tile class
# ------------------------------


class Tile(object):
    """One tile on the Sudoku grid.
    Public attributes (read-only): value, which will be either
    UNKNOWN or an element of CHOICES; candidates, which will
    be a set drawn from CHOICES.  If value is an element of
    CHOICES,then candidates will be the singleton containing
    value.  If candidates is empty, then no tile value can
    be consistent with other tile values in the grid.

    value and candidates are public read-only attributes; change them
    only through the access methods set_value and eliminate.
    """

    def __init__(self, row: int, col: int, value=UNKNOWN):
        assert value == UNKNOWN or value in CHOICES
        self.row = row
        self.col = col
        self.listeners = []
        self.set_value(value)

    def add_listener(self, listener: TileListener):
        """Listener will be notified of changes"""
        self.listeners.append(listener)

    def notify_all(self, event: TileChanged):
        """Notify each MVC listener that something has happened"""
        for listener in self.listeners:
            listener.notify(event)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return "Tile({},{},'{}')".format(self.row, self.col, self.value)

    def set_value(self, value, guess=False):
        if value in CHOICES:
            self.value = value
            self.candidates = set([value])
        else:
            self.value = UNKNOWN
            self.candidates = set(CHOICES)
        if guess:
            self.notify_all(TileGuessed(self))
        else:
            self.notify_all(TileChanged(self))

    def could_be(self, value: str) -> bool:
        """Could this tile take the value
        return value in self.candidates
        """
        return value in self.candidates

    def eliminate(self, choices: Set[str]) -> bool:
        """Eliminate the choices from candidates for
        this tile.  May result in either setting the
        value of this tile (if only one candidate remains)
        or making this tile inconsistent. Triggers a
        Changed event if there is any change.
        Returns True iff value is changed
        """
        # Careful! If you want to compare the value
        # of candidates before and after the operation,
        # you'll need to make a *copy* of the set, because
        # sets are mutable!

        copy = self.candidates.copy()

        self.candidates -= choices

        if self.candidates == copy:
            return False
        if len(self.candidates) == 1:
            popped = self.candidates.pop()
            self.set_value(popped)
            self.notify_all(TileChanged(self))

            return True
        elif self.candidates != copy:
            self.notify_all(TileChanged(self))

            return True
        else:
            return False

    def attend(self):
        """This tile is currently an object of attention"""
        self.notify_all(TileAttend(self))

    def unattend(self):
        """Done attending to this tile"""
        self.notify_all(TileUnattend(self))

# Design notes:
#    We want different kinds of tile events to guide
# view components in what to display (without putting
# those view design decisions here). I have chosen to
# create different TileEvent subclasses to indicate
# the event types.
#
# An alternative would be to pass a data value to indicate
# the event type. We could define symbolic constants
# to reduce the chance of hard-to-debug typographical errors,
# and we could use a Python Enum class to define those
# symbolic constants.  Enums do not act like other classes in
# Python, so I am reluctant to introduce them in this project.
#
# Using subclasses as I have here is almost like defining an
# Enum.  An advantage is that we could, if we needed to,
# add additional fields in a subclass for a particular event
# type.  A disadvantage is that we need to use the isinstance()
# method (usually in the view component) to determine which
# event type it is.
