"""
Test harness:
   Utility functions for writing test cases in Python programs.
   
   Python has a standard module, unittest, that provides a more
   powerful but but more complex testing framework. This module
   is designed to be very simple.

	testEQ checks a test case for predicted result
	test_approx checks a test case for approximately predicted result
	testRaise checks a test case for raising an expected exception

   Author: M Young, michal@cs.uoregon.edu
   October 2012 for CIS 210 at U. Oregon; 
     revised Fall 2014 (added approximate tests for floating point)
"""

def testEQ( desc, actual, expect ) : 
    """General framework for running a single test case
    with an expected result.  Prints a log message depending
    on whether the actual result was the same as the expected result.
    Args: 
        desc: Description of the test case
        actual:  Actual result (should be same as expected)
        expect:  Expected result
    """
    try: 
       if actual == expect : 
           print("   Passed -- ",desc, " result: ", actual)
       else: 
           print("***FAILED*** ", desc, " Expected: |", expect, 
               "| but got |", actual, "|")
    except Exception as E:
         print("***FAILED WITH EXCEPTION***", desc, E)

# Approximately equal.  We simply look for differences
# within some EPSILON.  Default EPSILON is 0.0001, but it
# can be reset

global EPSILON  
EPSILON = 0.0001

def test_approx(desc, actual, expect):
    """Run a single test case
    with an expected result.  Prints a log message depending
    on whether the actual result was within EPSILON of the
    expected result.
    Args: 
        desc: Description of the test case
        actual:  Actual result (should be near expected)
        expect:  Expected result
    """
    try:
       delta = abs(actual - expect)
       if delta < EPSILON : 
           print("   Passed -- ",desc, " result: ", actual, "~", expect)
       else: 
           print("***FAILED*** ", desc, " Expected: |", expect, 
               "| but got |", actual, "|")
    except Exception as E:
         print("***FAILED WITH EXCEPTION***", desc, E)

def testRaise(desc, kind, func):
    """Make sure an expected exception is raised.
    
    Args:
        desc: Description of the test case
        func: A function to call
    """
    try:
        func()
        print("***FAILED TO RAISE EXCEPTION***", desc)
    except kind as E:
        print("   Raised expected exception --", desc)
        print("    " + str(E))
    except Exception as E:
        print("***WRONG EXCEPTION**", str(E), desc)
    
