"""
Reading and writing Sudoku boards.  We use the minimal
subset of the SadMan Sudoku ".sdk" format,
see http://www.sadmansoftware.com/sudoku/faq19.php

Author: M Young, January 2018
"""

import sdk_board
import typing
from typing import List, Union
import sys
from io import IOBase


class InputError(Exception):
    pass


def read(f: Union[IOBase, str], board: sdk_board.Board=None) -> sdk_board.Board:
    """Read a Sudoku board from a file.  Pass in a path
    or an already opened file.  Optionally pass in a board to be
    filled.
    """
    if isinstance(f, str):
        f = open(f, "r")
    if board is None:
        board = sdk_board.Board()
    values = []
    for row in f:
        row = row.strip()
        values.append(row)
        if len(row) != 9:
            raise InputError("Puzzle row wrong length: {}"
                             .format(row))
    if len(values) != 9:
        raise InputError("Wrong number of rows in {}"
                         .format(values))
    board.set_tiles(values)
    return board


def write(board: sdk_board.Board, f: IOBase=sys.stdout):
    """Print the board"""
