##import argparse
##
##
##def job(dict_file_name):
##    print(type(dict_file_name))
####def jumbler(jumble, dict_file_name):
####    print(wordlist)
####
##def main():
####    """
####    collect command arguments and invoke jumbler()
####    inputs:
####        none, fetches arguments using argparse
####    effects:
####        calls jumbler()
####    """
##    parser = argparse.ArgumentParser(description="Solve a jumble (anagram)")
####    parser.add_argument("jumble", type=str, help="Jumbled word (anagram)")
##    parser.add_argument("wordlist", type=str,
##                        help="A text file containing dictionary words, one word per line.")
####
####    
####
##    args = parser.parse_args()  # gets arguments from command line
####    jumble = args.jumble
##    wordlist = args.wordlist
####    dict_file_name = open("wordlist", "r")
####    jumbler(jumble, wordlist)
##    dict_file_name = open(wordlist, "r")
##    dict_file_name = dict(dict_file_name)
##    job(dict_file_name)
##
##    dict_file_name.close
####
##if __name__ == "__main__":
##    main()     
####

dict_file_name = "dict.txt"
wordlist = {}
with open(dict_file_name, "r") as f:
    for line in f:
        split_line = line.split()
        wordlist[str(split_line[0])] = ",".join(split_line[1:])

print(wordlist)
