"""
Tests for Sudoku solver.
"""
import unittest

import sdk_tile
import sdk_board
import sdk_solver
import sdk_io


class test_tile_ops(unittest.TestCase):
    """Tests for sdk_tile.py"""

    def test_constructor_default(self):
        tile = sdk_tile.Tile(3, 3)
        self.assertEqual(tile.value, sdk_tile.UNKNOWN)
        self.assertEqual(tile.candidates, set(sdk_tile.CHOICES))
        for sym in ["1", "2", "3", "7", "8", "9"]:
            self.assertTrue(tile.could_be(sym))
        for sym in [".", "x", "0"]:
            self.assertFalse(tile.could_be(sym))

    def test_constructor_unknown(self):
        tile = sdk_tile.Tile(3, 3)
        self.assertEqual(tile.value, sdk_tile.UNKNOWN)
        self.assertEqual(tile.candidates, set(sdk_tile.CHOICES))
        for sym in ["1", "2", "3", "7", "8", "9"]:
            self.assertTrue(tile.could_be(sym))
        for sym in [".", "x", "0"]:
            self.assertFalse(tile.could_be(sym))

    def test_choice_removal(self):
        tile = sdk_tile.Tile(0, 0)
        self.assertEqual(tile.value, sdk_tile.UNKNOWN)
        self.assertEqual(tile.candidates, set(sdk_tile.CHOICES))
        tile.eliminate(set(["3", "4", "5"]))
        self.assertEqual(tile.candidates,
                         set(["1", "2", "6", "7", "8", "9"]))
        tile.eliminate(set(["1", "2", "6"]))
        self.assertEqual(tile.candidates, set(["7", "8", "9"]))
        self.assertTrue(tile.could_be("8"))
        self.assertFalse(tile.could_be("3"))
        self.assertEqual(tile.value, sdk_tile.UNKNOWN)
        tile.eliminate(set(["8", "9"]))
        self.assertEqual(tile.value, "7")
        self.assertEqual(tile.candidates, set(["7"]))


naked_single_example = [
    ".........", "......1..", "......7..",
    "......29.", "........4", ".83......",
    "......5..", ".........", "........."]

naked_single_propagated = [
    ".........", "......1..", "......7..",
    "......29.", "........4", ".83...6..",
    "......5..", ".........", "........."]

hidden_single_example = [
    ".........", "...2.....", ".........",
    "....6....", ".........", "....8....",
    ".........", ".........", ".....2..."]

hidden_single_propagated = [
    ".........", "...2.....", ".........",
    "....6....", "....2....", "....8....",
    ".........", ".........", ".....2..."]

wikipedia_example = [
    "53..7....", "6..195...", ".98....6.",
    "8...6...3", "4..8.3..1", "7...2...6",
    ".6....28.", "...419..5", "....8..79"]
wikipedia_solved = [
    "534678912", "672195348", "198342567",
    "859761423", "426853791", "713924856",
    "961537284", "287419635", "345286179"]
wikipedia_wrong = [
    "534678912", "672195348", "198342567",
    "859761423", "426853791", "713924856",
    "961537284", "287419635", "345285179"]


class test_board_ops(unittest.TestCase):
    """Tests for sdk_board.py"""

    def test_constructor(self):
        """Constructor creates empty board"""
        board = sdk_board.Board()
        self.assertEqual(len(board.tiles), 9)
        for row in board.tiles:
            self.assertEqual(len(row), 9)
        # Each tile should appear in 3 groups (row, column, block)
        board.set_tiles(naked_single_example)
        self.assertEqual(board.as_list(), naked_single_example)
        three_count = 0
        for group in board.groups:
            for tile in group.tiles:
                if tile.value == '3':
                    three_count += 1
        self.assertEqual(three_count, 3)

    def test_properties(self):
        board = sdk_board.Board()
        board.set_tiles(wikipedia_example)
        self.assertTrue(board.is_consistent())
        self.assertFalse(board.is_solved())
        board.set_tiles(wikipedia_solved)
        duplicate_reports = board.duplicates()
        self.assertEqual(duplicate_reports, [])
        self.assertTrue(board.is_consistent())
        self.assertTrue(board.is_solved())
        board.set_tiles(wikipedia_wrong)
        self.assertFalse(board.is_solved())
        self.assertFalse(board.is_consistent())


class test_constraint_propagation(unittest.TestCase):
    """Solving by constraint propagation"""

    def test_naked_single(self):
        board = sdk_board.Board()
        board.set_tiles(naked_single_example)
        sdk_solver.propagate(board)
        self.assertEqual(board.as_list(), naked_single_propagated)

    def test_hidden_single(self):
        board = sdk_board.Board()
        board.set_tiles(hidden_single_example)
        sdk_solver.propagate(board)
        self.assertEqual(board.as_list(), hidden_single_propagated)

    def test_constraint_propagation(self):
        board = sdk_io.read("data/nakedhiddensingle5.sdk")
        sdk_solver.propagate(board)
        self.assertEqual(board.as_list(),
                         ["381429567", "427685193", "965371248",
                          "873912654", "214856739", "596743812",
                          "648597321", "139268475", "752134986"])


if __name__ == "__main__":
    unittest.main()
