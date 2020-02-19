"""
Solve a jumble (anagram) by checking against each word in a dictionary
Authors: Noah Tigner   

Usage: python3 jumbler.py jumbleword wordlist.txt
"""

import argparse

def jumbler(jumble, dict_file_name):
    """
    compare a jumbled anagram to a dictionary to find matches.
    inputs:
        jumble: the given jumbled anagram
        dict_file_name: the file containing the dictionary of words
    output:
        prints the match(es) for the jumble as well as the amount of
        words in the dictionary
    """

    matches = 0     # initializing a variable to count the matches
    count  = 0      # initializing a variable to count the number of words in the file

    for word in dict_file_name: # read each word in the file
        word = word.strip()
        count += 1
        if sorted(word) == sorted(jumble):  # compare each word to 'jumble'
            matches += 1        # increment matches
            print(word)
            
    if matches == 1:            # print the matches
        fmt = "1 match in {} words"
        print(fmt.format(count))
    elif matches > 1:
        fmt = "{} matches in {} words"
        print(fmt.format(matches, count))
    else:
        print("No matches")
        

def main():
    """
    collect command arguments and invoke jumbler()
    inputs:
        none, fetches arguments using argparse
    effects:
        calls jumbler()
    """
    parser = argparse.ArgumentParser(description="Solve a jumble (anagram)")
    parser.add_argument("jumble", type=str, help="Jumbled word (anagram)")
    parser.add_argument('wordlist', type=str,
                        help="A text file containing dictionary words, one word per line.")
    args = parser.parse_args()  # gets arguments from command line
    jumble = args.jumble
    wordlist = args.wordlist

    dict_file_name = open(wordlist, "r")    # open the file
    jumbler(jumble, dict_file_name) # call jumbler
    dict_file_name.close        # close the file

if __name__ == "__main__":
    main()     

    

    

