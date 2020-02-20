w = 4
n = 8
INF = float("inf")


min_cost = [[0 for i in range(w+1)] for j in range(n+1)] 
  
# fill 0th row with infinity 
for i in range(w+1): 
    min_cost[0][i] = INF 

# fill 0th column with 0 
for i in range(1, n+1): 
    min_cost[i][0] = 0

for i in min_cost:
    print(*i)

################################################################

m_cost = []
for i in range(n+1):
    # m_cost.append([])
    # for j in range(n+1):
    #     m_cost[i][j].append(0)
    m_cost.append([0 for i in range(w+1)])

for i in range(w+1): 
    m_cost[0][i] = INF 



print('#'*32)
for i in m_cost:
    print(*i)
