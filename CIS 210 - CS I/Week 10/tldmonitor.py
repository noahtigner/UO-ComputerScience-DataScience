"""
Monitor web accesses by top-level domain for a specified time window.
Author:  #FIXME
Credits: #FIXME

Given a web log file and begin and end dates, compute the percentage of
web accesses, categorized by top-level domain, and display on the standard
output.
"""

import argparse

class Date:

    def __init__(self, str):
        """
        The constructor for an instance of the Date class.
        It receives one argument, a string in the format 'mm/dd/yyyy'.
        If the string is in the wrong format (not three integers separated
            by '/'), or if mm < 1 or mm > 12, or if dd < 1 or dd > number
            of days in that month, or if yyyy < 1, the constructor
            should raise an Exception with a string of the form:
            'mm/dd/yyyy: incorrectly formatted date string', where mm/dd/yyyy
            is replaced by the string that was passed as an argument
        Args:
            str - string, date of the form 'mm/dd/yyyy'
        Returns:
            nothing
        Effects:
            stores away month, day, and year in 'self' for future use
        Raises:
            Exception if the string received is incorrectly formatted
        """
        #FIXME - implement this method according to the docstring
        #Note - you may assume that every February has 29 days when
        #       checking that you have received a legal date string

    def __lt__(self, other):
        """
        Boolean function, returns True if self < other, False otherwise
        Args:
            self: Date instance to compare against other
            other: Date instance to which self is compared
        Returns:
            boolean, True if self < other, False otherwise
        """
        #FIXME - replace the following statement with your implementation
        return False

    def __gt__(self, other):
        """
        Boolean function, returns True if self > other, False otherwise
        Args:
            self: Date instance to compare against other
            other: Date instance to which self is compared
        Returns:
            boolean, True if self > other, False otherwise
        """
        #FIXME - replace the following statement with your implementation
        return False

    def __eq__(self, other):
        """
        Boolean function, returns True if self == other, False otherwise
        Args:
            self: Date instance to compare against other
            other: Date instance to which self is compared
        Returns:
            boolean, True if self == other, False otherwise
        """
        #FIXME - replace the following statement with your implementation
        return False

def main():
    parser = argparse.ArgumentParser(description="Monitor net accesses by TLD")
    parser.add_argument("Start", type=str, help="Start date for statistics")
    parser.add_argument("Stop", type=str, help="End date for statistics")
    parser.add_argument('log_file', type=argparse.FileType('r'),
                help = "Name of web log file")
    args = parser.parse_args()

    beg_date = Date(args.Start)
    end_date = Date(args.Stop)

    #FIXME - replace the following statement with your implementation
    print('I have not yet implemented this code')

if __name__ == "__main__":
    main()
