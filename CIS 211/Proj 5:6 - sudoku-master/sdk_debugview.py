"""
A view component designed for debugging Sudoku tactics.

This view can be attached to a board instead of or
in addition to a graphical viewer like sdk_display.
It prints (voluminous, potentially annoying) textual
information about operations and the state of the board.
You may want to combine it with debugging log data.

Author: M Young, January 2018 for CIS 211
"""

# Peer classes from model
import sdk_board
import sdk_tile

# Sudoku boards are always 9x9. The symbolic constants just help clarify
# the code a little, and would help us find dependency if we ever adapted
# this to a related game like ken-ken.
NROWS = 9
NCOLS = 9

# In the graphical display we have a view object for each tile. In this
# view we are interested in groups of tiles, so we have a single
# view object for the whole board.


class Board(object):
    """View of board.Board"""

    def __init__(self, model: sdk_board.Board):
        """Create a view of the board.
        Width and height are dimensions in pixels.
        """
        self.model = model
        for row in model.tiles:
            for tile in row:
                tile.add_listener(self)
        print("**Initial board: \n{}\n***\n\n".format(model))
        self.attending: Sequence[sdk_tile.tile] = []
        self.between_groups = True

    def _update(self, event: sdk_tile.TileEvent):
        """What is happening?"""
        if isinstance(event, sdk_tile.TileAttend):
            if self.between_groups:
                self.between_groups = False
                print("\n*** Group ***")
            self._show_tile(event.tile)
            self.attending.append(event.tile)

        elif isinstance(event, sdk_tile.TileUnattend):
            # When we drop attention, we drop for the whole group
            self.attending = []
            self.between_groups = True
        elif isinstance(event, sdk_tile.TileChanged):
            if self.between_groups:
                self.between_groups = False
            print("**Updated tile {},{}"
                  .format(event.tile.row, event.tile.col))
            self._show_tile(event.tile)

    def _show_tile(self, tile: sdk_tile.Tile):
        """Show tile in a useful format for debugging"""
        # Candidates in a format for eyeballing
        candidate_list = []
        for value in sdk_tile.CHOICES:
            if tile.could_be(value):
                candidate_list.append(value)
            else:
                candidate_list.append("_")
        candidates = "".join(candidate_list)
        print("Tile {} / {}".format(tile, candidates))

    def notify(self, event: sdk_tile.TileEvent):
        self._update(event)

    def close(self):
        pass
