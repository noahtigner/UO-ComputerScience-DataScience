import sys

class Graph:
    def __init__(self, vertices): 
        self.V = vertices

        # Adjacency List: a set of adjacent nodes for each node in V
        self.graph = [ set([]) for i in range(self.V)]


    
    def add_edge(self, source, destination):
        # Add adjacent node (destination) to the source node's adjacency list
        self.graph[source].add(destination)

    def print(self):
        # Print the adjacency lists. Used for testing
        for i in range(self.V):
            print("Node {}'s Neighbors: {}".format(i, self.graph[i]))





if __name__ == "__main__": 

    # Number of edges and vertices from file
    N = int(sys.stdin.readline())   # N = V = number of nodes/vertices
    M = int(sys.stdin.readline())   # M = E = number of unweighted edges
    g = Graph(N)
    
    # Add edges from file
    for line in range(M):
        edge = sys.stdin.readline().split()
        g.add_edge(int(edge[0])-1, int(edge[1])-1)

    # [min length path, max length path] for each node
    path_lengths = {}

    # [number of shortest paths, number of longest paths] for each node
    path_numbers = {}


    path_lengths[0] = [0, 0]
    path_numbers[0] = [1, 1]
    for m in range(1, N):
        path_lengths[m] = [0, 0]
        path_numbers[m] = [0, 0]
    
    g.print()

  
    for i in range(N):
        
        if len(g.graph[i]) > 0:

            shortest = path_lengths[i][0] + 1
            longest = path_lengths[i][1] + 1

            paths = path_numbers[i]

            for j in list(g.graph[i]):
                
                if path_lengths[j][0] == 0:
                    path_lengths[j][0] = shortest
                    path_numbers[j][0] = paths[0]
                elif path_lengths[j][0] == shortest:
                    path_numbers[j][0] = path_numbers[j][0] + paths[0]
                elif path_lengths[j][0] > shortest:
                    path_lengths[j][0] = shortest
                    path_numbers[j][0] = paths[0]

                if path_lengths[j][1] == 0:
                    path_lengths[j][1] = longest
                    path_numbers[j][1] = paths[1]
                elif path_lengths[j][1] == longest:
                    path_numbers[j][1] = path_numbers[j][1] + paths[1]
                elif path_lengths[j][1] < longest:
                    path_lengths[j][1] = longest
                    path_numbers[j][1] = paths[1]
                
                print("Min {}".format(shortest))
                print("Max {}".format(longest))
    

    print("*"*32)
    print(shortest)
    print(paths[0])
    print(longest)
    print(paths[1])

   
