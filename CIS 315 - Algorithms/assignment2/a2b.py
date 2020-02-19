import sys

class Graph:
    def __init__(self, vertices): 
        self.V = vertices
        self.graph = {n: [] for n in range(self.V)}

    def add_edge(self, source, destination):
        # Add adjacent node (destination) to the source node's adjacency list
        self.graph[source].append(destination)

    def print(self):
        # Print the adjacency lists. Used for testing
        for i in range(self.V):
            print("Node {}: {}".format(i, self.graph[i]))


if __name__ == "__main__": 

    # Number of edges and vertices from file
    N = int(sys.stdin.readline()) + 1 # N = V = number of nodes/vertices
    M = int(sys.stdin.readline())   # M = E = number of unweighted edges
    g = Graph(N)
    
    # Add edges from file
    for line in range(M):
        edge = sys.stdin.readline().split()
        g.add_edge(int(edge[0]), int(edge[1]))

    g.print()

    """
    I made 2 dictionaries. They both hold lists. 
    One holds [min length path, max length path] for each node. 
    The other holds [number of shortest paths, number of longest paths] for each node.
    """

    min_max = {}
    num_paths = {}

    """
    I initialize all the vals in min_path to [0,0] 
    and every one in num_paths except one which is [1,1] to [0,0] too. 
    """
    """
    min_max[0] = [0, 0]
    num_paths[0] = [1, 1]
    for i in range(1, N+ 1):
        min_max[i] = [0, 0]
        num_paths[i] = [0, 0]
    """
    for i in range(1, N+1):
        min_max[i] = [0, 0]
        if i == 1:
            num_paths[i] = [1, 1]
        else:
            num_paths[i] = [0, 0]

    
    """
    Then I loop through the vertices and for each one n 
    if it has any adjacencies I get the list of them, 
    then I make the variables min = min_path[n][0]+1 and max = min_path[n][1]+1 
    and paths = num_paths[n]. 
    Then from there I loop through each one of the adjacencies.
    """
  
    #alist = g.graph[0]
  

    for n in range(1, N):
        if n in g.graph:

            #if len(g.graph[n]) > 0:

            adj_list = g.graph[n]

            
            min = min_max[n][0] + 1
            max = min_max[n][1] + 1
            paths = num_paths[n]
        else:
            continue

        for j in adj_list:

            print("[{}][{}] [0]: {}".format(n, j, min_max[j][0]))

            
            if min_max[j][0] == 0:
                min_max[j][0] = min
                num_paths[j][0] = paths[0]
            elif min_max[j][0] == min:
                num_paths[j][0] = num_paths[j][0] + paths[0]
            elif min_max[j][0] > min:
                min_max[j][0] = min
                num_paths[j][0] = paths[0]
           
            if min_max[j][1] == 0:
                min_max[j][1] = max
                num_paths[j][1] = paths[1]
            elif min_max[j][1] == max:
                num_paths[j][1] = num_paths[j][1] + paths[1]
            elif min_max[j][1] < max:
                min_max[j][1] = max
                num_paths[j][1] = paths[1]
                

    print(min_max[N-1][0])
    print(num_paths[N-1][0])
    print(min_max[N-1][1])
    print(num_paths[N-1][1])
    
    

