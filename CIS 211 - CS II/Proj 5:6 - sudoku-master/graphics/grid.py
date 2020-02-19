"""
Grid display.  

Displays a rectangular grid of cells, organized in rows and columns
with row 0 at the top and growing down, column 0 at the left and 
growing to the right.

Uses the simple graphics module provided by Zelle, which in turn 
is built on the Tk graphics package (and which should therefore be 
available on all major Python platforms, including Linux, Mac, and 
all flavors of Windows at least back to XP).  Requires Python 3.6 
or greater due to use of type annotations and module 'typing'. 

Author: Michal Young (michal@cs.uoregon.edu), October 2012, 
for CIS 210 at University of Oregon.  Revised November 2013
for Sudoku with subgrids. Revised January 2018 for
CIS 211. 
"""
from graphics.graphics import *
# Python 3.6+: Gradual typing
import typing

BLACK = color_rgb(0,0,0)
WHITE = color_rgb(255,255,255)
GREY = color_rgb(200,200,200)

class Grid(object):
    """Generic grid of rectangles, for Sudoku, Naughts and Crosses, etc.
    Rows and columns are numbered from 0 to n-1, and
    rows are numbered from the top down.
    """

    def __init__(self, width: int, height: int,
                 nrows: int, ncols: int, title: str = "Untitled",
                 background = color_rgb(255, 255, 255)):
        """Create a view of the grid. 
        Width and height are dimensions in pixels. 
        """
        self.width = width
        self.height = height
        self.nrows = nrows
        self.win = GraphWin(title, width, height)
        bkgrnd = Rectangle( Point(0,0), Point(width,height) )
        bkgrnd.setFill( background ) 
        self.cell_width = width / ncols
        self.cell_height = height / nrows

    def fill_cell(self, row: int, col: int, color):
        """Fill cell[row,col] with color.
        Args: 
        row:  which row the selected cell is in.  Row 0 is the top row, 
           row 1 is the next row down, etc.  Row should be between 0 
           and one less than the number of rows in the grid. 
        col:  which column the selected cell is in.  Column 0 is 
           the leftmost row, column 1 is the next row to the right, etc. 
           Col should be between 0 and one less than the number of columns
           in the grid. 
        color: What color to fill fill the selecte cell with.  
        """
        left = col * self.cell_width
        right = (col + 1) * self.cell_width
        top = row * self.cell_height
        bottom = (row+1) * self.cell_height
        mark = Rectangle( Point(left,bottom), Point(right,top) )
        mark.setFill(color)
        mark.draw(self.win)

    def label_cell(self, row, col, text, color=BLACK):
        """Place text label on cell[row,col].
        Args: 
        row:  which row the selected cell is in.  Row 0 is the top row, 
            row 1 is the next row down, etc.  Row should be between 0 
            and one less than the number of rows in the grid. 
        col:  which column the selected cell is in.  Column 0 is 
           the leftmost row, column 1 is the next row to the right, etc. 
           Col should be between 0 and one less than the number of columns
           in the grid. 
        text: string (usually one character) to label the cell with
        color: Color of text label
        """
        xcenter = (col + 0.5) * self.cell_width
        ycenter = (row + 0.5) * self.cell_height
        label = Text( Point(xcenter, ycenter), text)
        label.setFace("helvetica")
        label.setSize(20)  ## Is there a better way to choose text size? 
        label.setFill(color)
        label.draw(self.win)

    def sub_grid_dim(self, rows, cols):
        """Divide each cell into rows x cols for sub-labeling
        (like "pencil marks" in Sudoku).
        Args:
        rows:  The number of rows of sub-cell in a cell.
        cols:  The number of columns of sub-cell in a cell.
        Returns: nothing
        Effects: Affects behavior of sub_label_cell
        """
        self.n_sub_rows = rows
        self.n_sub_cols = cols

    def sub_label_cell(self, row, col, sub_row, sub_col, text, color=BLACK):
        """Place label in subrow, subcol of row, col.
        Args:
        row:  Row of major grid (counting 0 as top row)
        col:  Column of major grid (counting 0 as leftmost column)
        sub_row:  Row in minor (interior) grid of cell
        sub_col:  Column in minor (interior) grid of cell
        text: Label (usually one character) to place there
        color: color of text
        """
        xcenter = self.cell_width * (col +  (sub_col + 0.5) / self.n_sub_cols)
        ycenter = self.cell_height * (row + (sub_row + 0.5)/ self.n_sub_rows)
        # print("Placing subgrid label at ({},{})".format(xcenter,ycenter))
        label = Text( Point(xcenter, ycenter), text)
        label.setFace("helvetica")
        label.setSize(10)  ## Is there a better way to choose text size? 
        label.setFill(color)
        label.draw(self.win)


    def close(self):
        """ Close the graphics window (shut down graphics). """
        self.win.close()
        
        
def main():
    """Smoke test"""
    grid = Grid(500,500,9,9)
    grid.sub_grid_dim(3,3)
    for row in range(9):
        for col in range(9):
            grid.fill_cell(row, col, color_rgb(200,200,200))
            grid.label_cell(row, col, "{},{}".format(row+1, col+1))

    input('Press enter to close')

if __name__ == "__main__":
    main()

