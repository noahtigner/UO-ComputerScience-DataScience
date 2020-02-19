"""
Sudoku solution tactics.  These include the
constraint propogation tactics and (in phase
two) the search-based solver.

Author: Noah Tigner
"""

from sdk_board import Board
import sdk_tile

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def naked_single(board: Board) -> bool:
    """As described in http://www.sadmansoftware.com/sudoku/nakedsingle.php
    Returns True iff some change has been made
    """
    logging.info("Applying naked single tactic")
    changed = False
    for group in board.groups:
        changed = group.naked_single_constrain() or changed
    return changed


def hidden_single(board: Board) -> bool:
    """As described in http://www.sadmansoftware.com/sudoku/hiddensingle.php
    Returns True iff some change has been made
    """
    logging.info("Applying hidden single tactic")
    changed = False
    for group in board.groups:
        changed = group.hidden_single_constrain() or changed
    return changed


def propagate(board: Board):
    """Propagate constraints until we either solve the puzzle,
    show the puzzle as given is unsolvable, or can make no more
    progress by constraint propagation.
    """
    logging.info("Propagating constraints")
    changed = True
    while changed:
        logging.info("Invoking naked single")
        changed = naked_single(board)
        if board.is_solved() or not board.is_consistent():
            return
        changed = hidden_single(board) or changed
        if board.is_solved() or not board.is_consistent():
            return
    return


def solve(board: Board) -> bool:
    """Main solver.  Initially this just invokes constraint
    propagation.  In phase 2 of the project, you will add
    recursive back-tracking search (guess-and-check with recursion).
    """
    log.debug("Called solve on board:\n{}".format(board))
    propagate(board)

    """
    Psuedocode for recursive backtracking:
    
    Bases:
    check if board is solved
        return True
    check if board is not consistent
        return False
        
    Initialize min candidates with a large number
    go through each tile on the board
        if the tile is empty and number of candidates is less then min candidates
            use this tile for further computation
    
    save the current board
    
    go through each candidate of the tile
        set the value of the tile with the candidate value
        call the function recursively with the current board
        if recursive call returns True
            return True
        else
            restore the board to its previous state
            
        otherwise return false
    """

    if board.is_solved():
        return True
    if not board.is_consistent():
        return False

    min_candidates = 10
    this = None

    for group in board.tiles:
        for tile in group:

            if tile.value == sdk_tile.UNKNOWN and len(tile.candidates) < min_candidates:
                this = tile
                min_candidates = len(tile.candidates)

    old_board = board.as_list()

    for candidate in this.candidates:
        this.set_value(candidate)
        if solve(board):
            return True
        else:
            board.set_tiles(old_board)

    return False
