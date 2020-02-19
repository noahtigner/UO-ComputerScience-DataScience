"""
Key press acquisition and interpretation.
This module is closely bound to the view
component. If a different view component is used,
a corresponding keypress module must be used
with it.  For example, we could have a pure textual
"glass tty" interface using curses, and in that case
we would need to use curses functions to obtain keystrokes.

"""
import view

# Internal codes for commands.

LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
UNMAPPED = "Unmapped"


# We can bind different areas of the keyboard to the
# commands. "Left", "right", etc are Tk codes for the
# arrow keys.  "jil," are a similar spatial pattern under
# the right hand.
KEY_BINDINGS = {  # Arrow keys, as interpreted by Tk and graphics.py
    "Left": LEFT, "Right": RIGHT, "Up": UP, "Down": DOWN,
    # left-hand --- some people use this pattern?
    "a": LEFT, "w": UP, "s": RIGHT, "z": DOWN,
    # VI / Vim editor movement
    "h": LEFT, "j": DOWN, "k": UP, "l": RIGHT,
    # Numeric keypad (one common mapping)
    "4": LEFT, "6": RIGHT, "8": UP, "2": DOWN
}


class Command(object):
    """Interpret keyboard input as commands from the
    set LEFT, RIGHT, UP, DOWN, and UNMAPPED for a
    key that does not have a binding.
    """

    def __init__(self, game_view):
        self.game_view = game_view

    def next(self):
        key = self.game_view.getKey()
        if key not in KEY_BINDINGS:
            return UNMAPPED
        else:
            return KEY_BINDINGS[key]
