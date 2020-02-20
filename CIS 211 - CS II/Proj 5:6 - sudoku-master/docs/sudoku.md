# Sudoku Solver

Sudoku is a popular logic-based number placement puzzle.For an example
and a bit of history, see
<a `  href="http://en.wikipedia.org/wiki/Sudoku">this wikipedia article on
Sudoku</a>. One of the interesting bits of history is the role of
  of a Sudoku puzzle generating program in popularizing Sudoku.
  Creating good puzzles is much harder than solving them!

Your program will read a Sudoku board that may be partially
  completed.  A board file contains 9 lines of 9 symbols, each of
  which is either a digit 0-9 or the 
full-stop symbol '.' (also called 'period'  or 'dot')
  to indicate a tile that has not been filled. Your program will first
  check for violations of Sudoku rules.  If the board is valid, 
  then your program will apply two 
simple tactics to fill in an as many open tiles as possible.  

A valid Sudoku solution has the following properties:

* In each of the 9 rows, each digit 1..9 appears
    exactly once.  (No duplicates, and no missing digits.)

* In each of the 9 columns, each digit 1..9 appears
    exactly once.
 
* The board can be divided into 9 subregion blocks, each 3x3.
    In each of these blocks, each digit 1..9 appears
    exactly once.

If the board contains only the symbols '1' through '9', the pigeonhole
principle ensures that these two properties are equivalent:

  * Each digit appears at least once in a row, column, and block

  * Each digit appears no more than once in a row, column, or block

If the board contains the symbols '1' through '9' and also the
wild-card symbol '.', we say it is incomplete.  We say an incomplete
board is *inconsistent* if any row, column, or block contains more
than one of the symbols '1' through '9', although it may contain
more than one wild-card symbol '.' indicating a choice yet to be
made. 

## The program

Your program will read an input file in the
basic form of the .sdk (Sadman Sudoku) format.
An input file will look like this:

```
...26.7.1
68..7..9.
19...45..
82.1...4.
..46.29..
.5...3.28
..93...74
.4..5..36
7.3.18...
```


If there are no duplicated entries in the board (and regardless
  of whether it is complete, with digits only, or has '.'
  characters indicating tiles yet to be filled), your program will
  proceed to the next step.  If there are duplicated elements,
  your program will report them. 

For example, suppose the input board contained this:

```
435269781
682571493
197834562
826195347
374682915
951743628
519326874
248957136
963418257
```

Then the interaction would look like this:

```
$ python3 sudoku.py board1.sdk
*** Tile at  5 0  is a duplicate of  9
*** Tile at  8 0  is a duplicate of  9
*** Tile at  3 8  is a duplicate of  7
*** Tile at  8 8  is a duplicate of  7
*** Tile at  6 2  is a duplicate of  9
*** Tile at  6 7  is a duplicate of  7
Sudoku FAIL
```

Note that when a duplicate is found, we report <em>all</em> instances
of the duplicate. 
For example, both 9's in the first column are reported as duplicates.

If you used the display option like this:
```
$ python3 sudoku.py --display boards/board1.sdk
```
then instead of the textual output, the program will display the board
with duplicate items marked: 
<img src="img/Sudoku-display.png" />


## Consistency checking
  
Because of the <a
  href="http://en.wikipedia.org/wiki/Pigeonhole_principle">pigeonhole
  principle</a> of mathematics, if the board contains only the 
  digits 1..9, the following two statements are
  equivalent: 

  *  None of the 9 digits 1..9 appears more than once in a
  row. 

  * Each of the 9 digits 1..9 appear at least once in a row.

It is therefore enough to  check for duplicates.  Checking for
missing entries is similar but slightly more complicated,
particularly since we are allowing "open" tiles with the 
"." symbol. 

## Completion with constraint propagation

If the board is consistent, then (and only then) your program
will apply two simple constraint propagation 
tactics to fill some of the empty tiles,
then print the resulting board.  These constraints are based
directly on the properties of a completed Sudoku puzzle,
viz., that each symbol must appear once but only once in each
row, column, and block. 

```
$ more board-sandiway-intermediate.sdk
.2.6.8...
58...97..
....4....
37....5..
6.......4
..8....13
....2....
..98...36
...3.6.9.
$ python3 sudoku.py board-sandiway-intermediate.sdk
.2.6.8...
58...97..
....4....
37....5..
6......74
..8....13
...92....
..98...36
...3.6.9.
```

In the example above, only a few tiles have been filled in,
  because only simple tactics have been used.  If you use the
   --display option, you can see progress in filling in tiles,
  including elimination of some candidates:

Constraint propagation alone is enough to solve
some easy puzzles: 

```
$ more board-incomplete-easy1.sdk
...26.7.1
68..7..9.
19...45..
82.1...4.
..46.29..
.5...3.28
..93...74
.4..5..36
7.3.18...
$ python3 sudoku.py board-incomplete-easy1.sdk
435269781
682571493
197834562
826195347
374682915
951743628
519326874
248957136
763418259
```

  <h1>What you must solve</h1>
  
  <p>We will consider the solving part of your program correct
  if it can solve all Sudoku
  puzzles that can be solved using only the &ldquo;<a
   href="http://www.sadmansoftware.com/sudoku/nakedsingle.htm">naked
  single</a>&rdquo; (also called &ldquo;singleton&rdquo; or
  &ldquo;sole candidate&rdquo;) and &ldquo;<a
   href="http://www.sadmansoftware.com/sudoku/hiddensingle.htm">hidden
  single</a>&rdquo; (also called &ldquo;unique candidate&rdquo;)
  tactics described at <a
   href="http://www.sadmansoftware.com/sudoku/solvingtechniques.htm">the
  SadMan Software site</a>. </p>
  

### Notes and hints on the Sudoku helper

It is difficult to avoid using the numbers 3 and 9 as magic numbers
  in a Sudoku program, and it is probably not worth trying. Since they
  have no other meaning aside from the size of the board and blocks
  within the board, using symbolic constants doesn't help.


