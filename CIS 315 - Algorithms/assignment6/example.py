import sys
  
INF = float("inf")
  
def MCAL(n, w, v, c): 

    ################################################################
    
    # min_cost = [[0 for i in range(w+1)] for j in range(n+1)] 
  
    # # fill 0th row with infinity 
    # for i in range(w+1): 
    #     min_cost[0][i] = INF 
  
    # # fill 0th column with 0 
    # for i in range(1, n+1): 
    #     min_cost[i][0] = 0

    # Fill table with 0s
    min_cost = []
    for i in range(n+1):
        min_cost.append([0 for i in range(w+1)])

    # 0th row is INF
    for i in range(w+1): 
        min_cost[0][i] = INF 

    ################################################################

    ################################################################
    # FIXME: Print food names
    # FIXME: formatting
    # TODO: rewrite
    # TODO: comment
  
    # now check for each weight one by one and fill the 
    # matrix according to the condition 
    for i in range(1, n+1): 
        for j in range(1, w+1): 
            # wt[i-1]>j means capacity of bag is 
            # less than weight of item 
            if (v[i-1] > j): 
                min_cost[i][j] = min_cost[i-1][j] 
  
            # here we check we get minimum cost either 
            # by including it or excluding it 
            else: 
                min_cost[i][j] = min(min_cost[i-1][j], min_cost[i][j-v[i-1]] + c[i-1]) 
    
    ################################################################

    ################################################################
    # TODO: rewrite
    # TODO: comment
  
    # exactly weight W can not be made by given weights 
    if(min_cost[n][w] == INF): 
        return "Not possible to spend exactly: {}".format(w)
    else: 
        return min_cost[n][w] 
    
    ################################################################
  

if __name__ == "__main__": 
    N = int(sys.stdin.readline())
    W = int(sys.stdin.readline())

    # print(N)
    # print(W)
    # TODO: comment

    v = []  # v[i] is i's cost
    c = []  # c[i] is i's calories
    s = []  # s[i] is i's name
    for i in range(N):
        # print(i)
        line = sys.stdin.readline().split()
        v.append(int(line[0]))
        c.append(int(line[1]))
        s.append(line[2])

    # for j in range(len(v)):
    #     print(str(v[j]) + ' ' + str(c[j]))

    print(MCAL(N, W, v, c)) 
  
