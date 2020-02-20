"""
squareroot.py:  Approximate pi with iterative function
Authors: Noah Tigner

CIS 210 assignment 2, Fall 2016. 
"""
import argparse      # Used in main program to get PIN code from command line
from test_harness import testEQ  # Used in CIS 210 for test cases
import math          # The math library from which our square root will be compared

## Constants used by this program

def my_sqrt(number, iterations):
    """
    Generate an iterative approximation to the square root of a number
    args:
        number:  positive number to calculate the square root of
        iterations: number of iterations to perform
    returns:
        approximate value of the square root
    """
    value = 1
    for i in range(iterations):
        value = 0.5 * (value + (number / value))
##value = round(value, 5)
    return value

##def calc_error(number, my_sqrt, iterations):
##    """
##    Calculates the percent error between my_sqrt and the math library's
##    sqrt() function
##    args:
##        number:  positive number to calculate the square root of
##        my_sqrt(): the function that returns the value
##        iterations: number of iterations to perform
##    returns:
##        the percent error rounded to two decimal places
##    """
##    print(math.sqrt(number), math)
##    value = float(my_sqrt(number, iterations))
##    print(value, "value")
##    error = round(100 * ((value / float(math.sqrt(number))) - 1), 2)
##    return error

def run_tests():
    """
    This function runs a set of tests to help you debug your
    program as you develop it.
    """
    print("**** TESTING --- 5 iterations for sqrt of 1, 10, 100, 1000, 10000")
    testEQ("1.0", my_sqrt(1.0, 5), 1.0)
    testEQ("10.0", my_sqrt(10.0, 5), 3.162277665175675)
    testEQ("100.0", my_sqrt(100.0, 5), 10.032578510960604)
    testEQ("1000.0", my_sqrt(1000.0, 5), 41.24542607499115)
    testEQ("10000.0", my_sqrt(10000.0, 5), 323.0844833048122)
    print("*** End of provided test cases.  Add some of your own? ****")

def main():
    """
    Interaction if run from the command line.
    Magic for now; we'll look at what's going on here
    in the next week or two. 
    """
    parser = argparse.ArgumentParser(description="Iterative approximation for square root")
    parser.add_argument("Number", type=float, help="number (a float)")
    parser.add_argument("-i", "--iterations", type=int, help="iterations (an int)")
    args = parser.parse_args()  # gets arguments from command line
    number = args.Number
    if number < 0:
        print("Square root undefined for", number)
        return
    iterations = args.iterations
    value = my_sqrt(number, iterations)
    true = math.sqrt(number)
    difference = math.fabs(value - true)
    if true == 0:
        fraction = 0
    else:
        fraction = difference / true
    fmt = "After {} iterations, sqrt({}) = {:.5f}; this represents {:.2%} error compared to the math library"
    print(fmt.format(iterations, number, value, fraction))
##    error = calc_error(number, my_sqrt, iterations)
##    print("After", iterations, "iterations, sqrt(", number, ") = ", value, "; this represents a", error, "% error compared to the math library")

if __name__ == "__main__":
    ##run_tests()
    main()


