"""
draw_barcode.py: Draw barcode representing a ZIP code using Turtle graphics
Authors: Noah Tigner

CIS 210 assignment 3, part 2, Fall 2016.
"""
import argparse	# Used in main program to obtain 5-digit ZIP code from command
                # line
import time	# Used in main program to pause program before exit
import turtle	# Used in your function to print the bar code

## Constants used by this program
SLEEP_TIME = 100	# number of seconds to sleep after drawing the barcode
ENCODINGS = [[1, 1, 0, 0, 0],	# encoding for '0'
             [0, 0, 0, 1, 1],	# encoding for '1'
             [0, 0, 1, 0, 1],   # encoding for '2'
             [0, 0, 1, 1, 0],	# encoding for '3'
             [0, 1, 0, 0, 1],	# encoding for '4'
             [0, 1, 0, 1, 0],	# encoding for '5'
             [0, 1, 1, 0, 0],	# encoding for '6'
             [1, 0, 0, 0, 1],	# encoding for '7'
             [1, 0, 0, 1, 0],	# encoding for '8'
             [1, 0, 1, 0, 0]	# encoding for '9'
            ]
SINGLE_LENGTH = 25	# length of a short bar, long bar is twice as long

def compute_check_digit(zip, my_turtle):
    """
    Compute the check digit for use in ZIP barcodes
    args:
        digits: list of 5 integers that make up zip code
    returns:
        check digit as an integer
    """
    digits = zip
    digits = "".join(digits)
    sum = 0
    for i in range(len(digits)):
        sum = sum + int(digits[i])
    check_digit = 10 - (sum % 10)
    if (check_digit == 10):
        check_digit = 0
    digit = check_digit
    draw_bar(my_turtle, digit)
    return check_digit

def draw_bar(my_turtle, digit):
    """
    Draws the lines with a variable lenght based on the provided
    digits.
    args:
        my_turtle: calls the turtle
        digit: the values needed to know to draw a line or double line
    returns:
        draws part of the barcode (when called)
    """
    my_turtle.left(90)
    if digit == 0:
        length = SINGLE_LENGTH
    else:
        length = 2 * SINGLE_LENGTH
    my_turtle.forward(length)
    my_turtle.up()
    my_turtle.backward(length)
    my_turtle.right(90)
    my_turtle.forward(10)
    my_turtle.down()

def draw_zip(my_turtle, zip):
    """
    Draw the digits of the barcode using the given zipcode
    args:
        my_turtle: calls the turtle to allow us to draw
        zip: the zip code provided by the command line
    returns:
        the barcode in the turtle graphics window
    """

    my_turtle.penup()   # move the turtle back so that the barcode is centered
    my_turtle.back(150)
    my_turtle.pendown()
    
    zip = str(zip)
    global ENCODINGS    # allows us to access the encodings
    digits = []
    digit = []

    digits += zip   # adds the zip to the empty list digits

    draw_bar(my_turtle, 1)  # this draws the starting gaurd rail

    for i in range(len(digits)):    # adds the encodings to the list
        digit = zip[i]
        digit = ENCODINGS[int(digit)]

        for i in range(len(digit)): # draws the digits       
            draw_bar(my_turtle, digit[i])

    for i in range(len(zip)):   # this draws the check digit
        compute_check_digit(zip[i], my_turtle)
        
    draw_bar(my_turtle, 1)  # this draws the ending gaurd rail

def main():
    """
    Interaction if run from the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("ZIP", type=int)
    args = parser.parse_args()
    zip = args.ZIP
    if zip <= 0 or zip > 99999:
        print("zip must be > 0 and < 100000; you provided", zip)
    else:
        my_turtle = turtle.Turtle() # assigns the turtle
        my_turtle.speed(100)    # speeds up the turtle
        draw_zip(my_turtle, zip)
        time.sleep(SLEEP_TIME)  # closes the turtle window after 30 seconds

if __name__ == "__main__":
    main()
