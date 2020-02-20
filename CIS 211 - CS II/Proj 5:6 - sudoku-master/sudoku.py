"""Sudoku solver with optional displays"""

import argparse

import sdk_board
import sdk_display
import sdk_debugview
import sdk_solver
import sdk_io

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def cli() -> object:
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Sudoku solver")
    parser.add_argument("-d", "--display", help="Graphical display",
                        action="store_true")
    parser.add_argument("-s", "--scan",
                        help="Show attention scan (only with --display)",
                        action="store_true")
    parser.add_argument("-t", "--text", help="Text monitor progress",
                        action="store_true")
    parser.add_argument("file", type=argparse.FileType('r'))

    args = parser.parse_args()
    return args


def main():
    args = cli()
    board = sdk_io.read(args.file)
    if args.display:
        display = sdk_display.Board(board, 400, 400, scan=args.scan)
    if args.text:
        monitor = sdk_debugview.Board(board)
    sdk_solver.solve(board)
    if board.is_solved():
        print("\nSolved!")
    else:
        print("\nNot solved")
    print(board)

    if args.display:
        input("Press enter to shut down")
        display.close
    if args.text:
        monitor.close()


if __name__ == "__main__":
    main()
