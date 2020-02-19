import sys

class Graph:
    
    def __init__(self, vertices): 
        self.V = vertices
        self.graph = {n: [] for n in range(self.V)} # list of adjacent nodes for each node
        self.path_lengths = {}  # [min length path, max length path] for each node
        self.path_count = {}    # [number of shortest paths, number of longest paths] for each node

    def add_edge(self, source, destination):
        # Add adjacent node (destination) to the source node's adjacency list
        self.graph[source].append(destination)

    def print(self):
        # Print the adjacency lists. Used for testing
        for i in range(self.V):
            print("Node {}: {}".format(i, self.graph[i]))



if __name__ == "__main__": 

    # Number of edges and vertices from file
    N = int(sys.stdin.readline())   # N = V = number of nodes/vertices
    M = int(sys.stdin.readline())   # M = E = number of unweighted edges
    g = Graph(N)
    
    # Add edges from file
    for line in range(M):
        edge = sys.stdin.readline().split()
        g.add_edge(int(edge[0])-1, int(edge[1])-1)  # Counting from 0

    # Initialize lengths and counts to 0 for all nodes except the first
    g.path_lengths[0] = [0, 0]
    g.path_count[0] = [1, 1]    
    for i in range(1, N):
        g.path_lengths[i] = [0, 0]
        g.path_count[i] = [0, 0]

    for node in range(N):
        
        for adjacent in g.graph[node]:
            # Finds Longest Path
            # For each node's adjacent node(s):
            #   if path length = original node's path length + 1
            #       increment count by the original node's count
            #   else if path length is longer:
            #       path length = original's length + 1
            #       path count = original's count
            #   else if the path is 0:
            #       path length becomes the previous' path + 1
            #       path count becomes original node's count

            if g.path_lengths[adjacent][1] == g.path_lengths[node][1] + 1:
                g.path_count[adjacent][1] = g.path_count[adjacent][1] + g.path_count[node][1]

            elif g.path_lengths[adjacent][1] < g.path_lengths[node][1] + 1:
                g.path_lengths[adjacent][1] = g.path_lengths[node][1] + 1
                g.path_count[adjacent][1] = g.path_count[node][1]
                
            elif g.path_lengths[adjacent][1] == 0:
                g.path_lengths[adjacent][1] = g.path_lengths[node][1] + 1
                g.path_count[adjacent][1] = g.path_count[node][1]

        for adjacent in g.graph[node]:
            # Same logic as above but for shortest path
            
            if g.path_lengths[adjacent][0] == g.path_lengths[node][0] + 1:
                g.path_count[adjacent][0] = g.path_count[adjacent][0] + g.path_count[node][0]
                
            elif g.path_lengths[adjacent][0] > g.path_lengths[node][0] + 1:
                g.path_lengths[adjacent][0] = g.path_lengths[node][0] + 1
                g.path_count[adjacent][0] = g.path_count[node][0]

            elif g.path_lengths[adjacent][0] == 0:
                g.path_lengths[adjacent][0] = g.path_lengths[node][0] + 1
                g.path_count[adjacent][0] = g.path_count[node][0] 

    # Counting from 0 so Nth node is N-1
    shortest = g.path_lengths[N-1][0]
    longest = g.path_lengths[N-1][1]
    s_count = g.path_count[N-1][0]
    l_count = g.path_count[N-1][1]

    print("Shortest Path: {}".format(shortest))
    print("Number of short paths: {}".format(s_count))
    print("Longest Path: {}".format(longest))
    print("Number of long paths: {}".format(l_count))