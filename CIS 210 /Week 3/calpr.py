"""
calpr.py: Print the calendar for a month.
Authors: Noah Tigner

Input is a month and a corresponding year. Output is a formatted
calendar for the given month.
Limitations: Treats February as always having 28 days.

CIS 210 assignment 3, Fall 2016
"""

import argparse     # Receives arguments from the command line
import datetime as dt    # To determine what day of week a month begins on

# Constants:

MONTHLEN = [ 0, # No month zero
             31, # January
             28, # February (ignoring leap years)
             31, # March
             30, # April
             31, # May
             30, # June
             31, # July
             31, # August
             30, # September
             31, # October
             30, # November
             31, # December
             ]

def calendar_print(month, year):
    """
    This function prints a calendar for a given month
    args:
        month, year
    returns:
        a properly formatted calendar for the given month and year
    """

    # What day of the week doe year, month begin on?
    a_date = dt.date(year, month, 1)
    starts_weekday = a_date.weekday()
    # a_date.weekday() gives 0=monday, 1=Tuesday, etc.
    # Roll to start week on Sunday
    starts_weekday = (1 + starts_weekday) % 7

    month_day = 1           # Next day to print
    last_day = MONTHLEN[month]  # Last day to print

    print(" Su Mo Tu We Th Fr Sa")

    # The first (perhaps partial) week
    for i in range(7):
        if i < starts_weekday:
            print("   ", end="")
        else:
            # Logic for printing one day, moving to the next
            print(format(month_day, "3d"), end = "")
            month_day += 1
    print() # Newline

    # The middle (full) weeks
    while last_day - month_day >= 7:
        for i in range(7):
            print(format(month_day, "3d"), end = "")
            month_day += 1
        else:
            print() # Newline

    # The last (partial) week (optional)
    for i in range(last_day - (month_day - 1)): # Find the number of days remaining
        print(format(month_day, "3d"), end = "")  # print the days remaining
        month_day += 1
    print()
    

def main():
    """
    Interaction if run from the command line.
    """
    parser = argparse.ArgumentParser(description = "Print calendar")
    parser.add_argument("month", type = int,
                        help = "Month number (1-12)")
    parser.add_argument("year", type = int,
                        help = "Year (1800-2525)")
    args = parser.parse_args()    # Gets arguments from the command line
    month = args.month
    year = args.year
    calendar_print(month, year)
    
if __name__ == "__main__":
    main()
