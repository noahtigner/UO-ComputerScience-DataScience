import sys

class Graph:
    def __init__(self, vertices): 
        self.V = vertices

        # Adjacency List: a set of adjacent nodes for each node in V
        self.graph = [ set([]) for i in range(self.V)]

        # Update these as the algorithm runs
        self.longest = 0
        self.shortest = sys.maxsize # Obscenely large
        self.num_longest = 0
        self.num_shortest = 0
    
    def add_edge(self, source, destination):
        # Add adjacent node (destination) to the source node's adjacency list
        self.graph[source].add(destination)

    def print(self):
        # Print the adjacency lists. Used for testing
        for i in range(self.V):
            print("Node {}'s Neighbors: {}".format(i, self.graph[i]))

    def bfs_paths(self, source, destination):
        # Queue: vertex, path[]
        queue = [(source, [])]

        # While !Q is empty
        while queue:
            (vertex, path) = queue.pop(0)

            for i in self.graph[vertex] - set(path):
                if i == destination:
                    # Once destination reached, check length of path and update if larger, smaller, or equal to either

                    if len(path) > self.longest:
                        self.longest = len(path)
                        self.num_longest = 1
                    elif len(path) == self.longest:
                        self.num_longest += 1

                    if len(path) < self.shortest:
                        self.shortest = len(path)
                        self.num_shortest = 1
                    elif len(path) == self.shortest:
                        self.num_shortest += 1

                else:
                    queue.append((i, path + [i]))

if __name__ == "__main__": 

    # Number of edges and vertices from file
    N = int(sys.stdin.readline())   # N = V = number of nodes/vertices
    M = int(sys.stdin.readline())   # M = E = number of unweighted edges
    g = Graph(N)
    
    # Add edges from file
    for line in range(M):
        edge = sys.stdin.readline().split()
        g.add_edge(int(edge[0])-1, int(edge[1])-1)

    # Paths from first node to last in topo order
    g.bfs_paths(0, N-1)

    if g.num_longest == 0 and g.num_shortest == 0:
        print("No paths exist")
    else:
        print("Shortest Path: {}".format(g.shortest+1)) # +1 because path doesn't count source
        print("Number of short paths: {}".format(g.num_shortest))
        print("Longest Path: {}".format(g.longest+1))   # +1 because path doesn't count source
        print("Number of long paths: {}".format(g.num_longest))