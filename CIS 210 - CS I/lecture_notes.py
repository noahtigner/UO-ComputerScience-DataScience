##from math import pi # imports pi so you can call pi instead of math.pi
##print(pi)
##
##print("{:.2f}".format(pi))  # rounds to 2 decimal places
##print("{:.3f}".format(pi))  # rounds to 3 decimal places
##
### Dictionaries:
### values stored in the container can be udexed using user-specified Keys
##faculty = {                                 # create the dictionary
##    "951234567": ["Joe", "Professor"]
##    "951765432": ["Sally", "Professor"]
##    }
## 
##faculty["951234568"] = ["Mabel", "Instructor"]  # add something to the dict
##
##del faculty["951765432"]            # delete something from the dict
##
##print(faculty)


## Friday Oct. 14 ..............................................................

# Opening Files
##my_data = open("mydata.txt", "r")
##for line in my_data:
##    print(line, end="")
##
##my_data.close()

# Functional Testing....
# Equivalence Classes

## Tuesday Oct. 25 ..............................................................

##def add_rec(aList):     # sum a list of numbers recursively
##    if len(aList) == 0:
##        return 0
##    if len(aList) == 1:
##        return aList[0]
##    return aList[0] + add_rec(aList[1:])


## Wednesday Oct. 25 ...........................................................

def data_mode(my_list):
    dict_of_counts = {}

    for item in my_list:
        if item in dict_of_counts:
            dict_of_counts[item] += 1
        else:
            dict_of_counts[item] += 1
            ..........






def data_freq_table(my_list):
    count = {}

    for item in my_list:
        if item in count:
            count{item] += 1
        else:
            count[item] += 1

        keys = list(count.keys())
        min_item = 0
        max_item = len(keys) - 1

        count_list = count.values()
        max_c = max(count_list)

        wn = turtle.Screen()
        chart_t = turtle.Turtle()
        wn.setworldcoordinates(-1, -1, max_item + 1, max_c + 1)
        chart_t.hideturtle()

    chart_t.up()
    chart_t.goto(0, 0)
    chart_t.down()
    chart_t.goto(max_item, 0)
    chartr_t.up()

    chart_t.goto(-1, 0)
    chart_t.write(str(keys[i]), font = ("Helvetica", 16, "bold"))
    chart_t.goto(i, 0)
    chart_t.down()
    ......
        
