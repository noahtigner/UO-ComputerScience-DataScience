"""
count.py: Count the number of occurrences of each major code in a file.
Author: Noah Tigner

Input is a file in which major codes (e.g., "CIS", "UNDL", "GEOG")
appear one to a line. Output is a sequence of lines containing major code
and count, one per major.

CIS 210 assignment 2, Fall 2016
"""

import argparse

def count_codes(majors_file):
    """
    This function counts the majors in a text file and
    returns them in a sorted list.
    args:
        majors_file: the file containing the list of majors
    returns:
        a new list with the majors sorted and counted
    """
    majors = [ ]

    for line in majors_file:
        majors.append(line.strip())

    majors = sorted(majors)
##    major_len = len(majors)
##    count = 1

    if len(majors) == 0:
        print(majors_file, "is empty")
        return
    
##    while major_len >= 1:
##        while major_len > 1 and majors[0] == majors[1]:
##            major = ''
##            major += majors[0]
##            count  = count + 1
##            if majors[0] == majors[1]:
##                del majors[0]
##                major_len = major_len - 1
##        while major_len >= 2 and majors[0] != majors[1]:
##            major = ''
##            major += majors[0]
##            print(major, count) 
##            count = 1
##            del majors[0]
##            major_len = major_len - 1
##        if major_len == 1:
##            count = 0
##            major = ''
##            major += majors[0]
##            count = count + 1
##            major_len = major_len - 1

    majors.append("This is not a legal major")      # sentinel element
    current_major = majors[0]                       # the check for an empty list
    
    count = 0
    for major in majors:
        if major == current_major:
            count += 1
        else:
            print(current_major, count)
            current_major = major
            count = 1
    
def main( ):
    """
    Interaction if run from the command line.
    Usage:  python3 counts.py  majors_code_file.txt
    """
    parser = argparse.ArgumentParser(description="Count major codes")
    parser.add_argument('majors', type=argparse.FileType('r'),
                        help="A text file containing major codes, one major code per line.")
    args = parser.parse_args()  # gets arguments from command line
    majors_file = args.majors
    count_codes(majors_file)
    
    
if __name__ == "__main__":
    main( )
