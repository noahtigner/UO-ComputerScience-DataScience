"""
Sudoku solver.
Author: Michal Young, 10-15 November 2012 for CIS 210
Author: Joe Sventek, 11-13 November 2015, minor modifications

Overall application control (including instantiation of 
graphical and/or textual views of progress).
"""
import sdkboard    # The Sudoku board  (model component)
import sdkdisplay  # Display of Sudoku board (view component)
import sdktactics  # Tactics for checking and solving sudoku
import sdktextview # Alternative display: spew text
import argparse    # Interpret command line


###
# Command line processing - the Pythonic way
###

parser = argparse.ArgumentParser(description="""
   Check a Sudoku board (complete or incomplete) to
   report whether it is correct or whether, on the
   contrary, there are duplicate digits in a row,
   a column, or a subsquare.  If there are no 
   errors, proceed to fill in as many open tiles
   as possible using the naked single and hidden 
   single tactics. """)

parser.add_argument('board', metavar="filename",
                    type=argparse.FileType('r'), 
                    help="file containing board description")
                    
parser.add_argument('--display', action="store_true", 
                    help="Display Sudoku board graphically")
                    
args = parser.parse_args()

###
# Main program logic
###

f = args.board
board = sdkboard.Board.from_file(f)

if args.display: 
    sdkdisplay.display(board)
else:
    sdktextview.display(board)
  
sdktactics.prepare(board)
if sdktactics.good_board():
    sdktactics.solve()
    print(board)
else:
    print("Sudoku FAIL")

if args.display: 
    input("Press enter to close down")



    
