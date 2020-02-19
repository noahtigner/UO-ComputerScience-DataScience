import sys
  
INF = float("inf")
  
def iter_MCAL(n, w, v, c, s): 

    # Initialize N*W table 
    min_cost = []
    for i in range(n+1):
        min_cost.append([0 for i in range(w+1)])
    # Set 0th row to INF
    for i in range(w+1): 
        min_cost[0][i] = INF 

    ind = []
    for i in range(w+1):
        ind.append(0)

    for i in range(1, n+1): 
        for j in range(1, w+1): 

            # v[i-1] > total weight
            if (v[i-1] > j): 
                min_cost[i][j] = min_cost[i-1][j] 
  
            else: 
                # Decides if the including the item would reduce the total cals
                if min_cost[i][j-v[i-1]] + c[i-1] < min_cost[i-1][j]:
                    ind[j-1] = i-1
                    min_cost[i][j] = min_cost[i][j-v[i-1]] + c[i-1]
                else:
                    min_cost[i][j] = min_cost[i-1][j]

    if(min_cost[n][w] == INF): 
        return "Not possible to spend exactly: {}".format(w), ind
    return min_cost[n][w], ind # list

def formatter(N, W, v, c, s):
    """ Formats Output """

    # Calls iterative dp alg
    minimum, li = iter_MCAL(N, W, v, c, s)

    # If not possible
    if not isinstance(minimum, int):
        print(minimum)

    else:
        print("""Possible to spend exactly: {}\nMinimum calories: {}""".format(W, minimum))

        # Prints whats in the knapsack
        i = 0
        while minimum > 0 & i < len(li):
            if li[-i] != -1: # and minimum - c[li[i]] > 0:
                counts[s[li[-i]]] += 1
                minimum -= c[li[-i]]
                # print(minimum)
            i += 1
        for i in counts:
            if counts[i] > 0:
                print("{} {}".format(i, counts[i]))

        
if __name__ == "__main__": 

    N = int(sys.stdin.readline())   # Number of menu items
    W = int(sys.stdin.readline())   # Number of cents (target weight)

    v = []  # v[i] = i's cost
    c = []  # c[i] = i's calories
    s = []  # s[i] = i's name
    counts = {} # name:count

    # Fill lists from file
    for i in range(N):
        line = sys.stdin.readline().split()
        v.append(int(line[0]))
        c.append(int(line[1]))
        s.append(line[2])
        counts[line[2]] = 0

    formatter(N, W, v, c, s) # Starts Algorithm
