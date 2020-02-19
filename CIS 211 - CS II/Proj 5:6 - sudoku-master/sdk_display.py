"""
Sudoku board display. 
Designed for a simple model/view/controller architecture, 
in which the board display knows about the sudoku board, 
and not vice versa.  Communication from the sudoku board
to the board display is by event notifications through 
registered listeners. 

Displays a rectangular grid of cells, organized in rows and columns
with row 0 at the top and growing down, column 0 at the left and 
growing to the right.  A sequence of unique colors for cells can 
be chosen from a color wheel, in addition to colors 'black' and 'white'
which do not appear in the color wheel. 

Author: M Young, Nov 10 2012 for CIS 210,
revised January 2018 for CIS 211
"""

# Peer classes from model
import sdk_board
import sdk_tile
# Graphics package based on Zelle's simple OO graphics
import graphics.grid
import graphics.graphics
from graphics.graphics import color_rgb

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Sudoku boards are always 9x9. The symbolic constants just help clarify
# the code a little, and would help us find dependency if we ever adapted
# this to a related game like ken-ken. 
NROWS = 9
NCOLS = 9


# Color scheme
# Background color white 
COLOR_BACKGROUND = "#ffffff"  
# Cells with an assigned value green
COLOR_KNOWN = "#ccffcc"
# Cells still unknown value beige 
COLOR_UNKNOWN = "#ffffcc"
# Current working group pink
COLOR_WORKING = "#ffccff"

class Board(object):
    """View of board.Board"""

    def __init__(self, model: sdk_board.Board, width: int, height: int,
                     scan=False):
        """Create a view of the board.
        Width and height are dimensions in pixels. 
        With scan=True, we highlight tiles that are the 
        current focus of attention ("attending"). 
        """
        self.model = model
        self.scan = scan
        # Sudoku board is always 9x9
        self.grid = graphics.grid.Grid(width, height, NROWS, NCOLS,
                                           title="Duck Sudoku")
        # We don't actually listen to the model board; each individual tile view
        # listens to its own model tile
        self.tiles = [ ]
        for row in model.tiles:
            for tile in row:
                self.tiles.append(Tile(self.grid, tile, scan=self.scan))

    def close(self):
        self.grid.close( )


class Tile(sdk_tile.TileListener):
    """View of a single tile"""

    def __init__(self, grid: graphics.grid.Grid, model: sdk_tile.Tile,
                     scan=False):
        self.grid = grid
        self.model = model
        self.row = model.row
        self.col = model.col
        self.scan = scan
        self.grid.sub_grid_dim(3,3)
        self._update(sdk_tile.TileChanged(self.model))
        self.model.add_listener(self)

    def _update(self, event: sdk_tile.TileEvent):
        # Color code the tiles to indicate groups and status
        if isinstance(event, sdk_tile.TileAttend):
            if self.scan: 
                self.grid.fill_cell(self.row, self.col, COLOR_WORKING)
                self._label()
        elif isinstance(event, sdk_tile.TileUnattend):
            if self.scan:
                self._color_by_status()
                self._label()
        elif isinstance(event, sdk_tile.TileChanged):
            self._color_by_status()
            self._label()
        else:
            raise ValueError("Unanticipated event type")
        
    def _color_by_status(self):
        if self.model.value == sdk_tile.UNKNOWN:
            self.grid.fill_cell(self.row, self.col, COLOR_UNKNOWN)
        else:
            self.grid.fill_cell(self.row, self.col, COLOR_KNOWN)
        

    def _label(self):
        if self.model.value == sdk_tile.UNKNOWN:
            self._pencil_marks()
        else:
            self.grid.label_cell(self.row, self.col, self.model.value)
        

    def _pencil_marks(self):
        """So-called 'pencil marks' are small digits indicating a possible 
        choice for a tile value.  We mark the possible choices in a 
        3x3 grid, leaving a blank for others. 
        """
        choices = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        for i in range(3):
            for j in range(3):
                    if self.model.could_be(choices[i][j]):
                        self.grid.sub_label_cell(self.row, self.col,
                                                     i, j, choices[i][j])


    def notify(self, event: sdk_tile.TileEvent):
        self._update(event)

