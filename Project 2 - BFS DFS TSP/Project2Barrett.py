# Stone Barrett
# CSE 545 Artificial Intelligence
# Project 2

# Importing useful tools
import time
from collections import defaultdict

# DFS

# Paths between connected cities
# Calculated using d = sqrt(((x2-x1)^2)+((y2-y1)^2))
# Hardcoded in
path12 = 21.048
path13 = 8.201
path14 = 25.951
path23 = 18.991
path34 = 24.833
path35 = 13.328
path45 = 17.251
path46 = 12.299
path47 = 13.126
path57 = 15.83
path58 = 31.912
path68 = 8.692
path79 = 8.31
path710 = 24.695
path89 = 13.636
path810 = 10.582
path811 = 16.207
path911 = 12.289
path1011 = 12.886

# Adjacency Matrix
graph = [   [0, 21.048, 8.201, 25.951, 10000, 10000, 10000, 10000, 10000, 10000, 10000  ],
            [10000, 0, 18.991, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000   ],
            [10000, 10000, 0, 24.833, 13.328, 10000, 10000, 10000, 10000, 10000, 10000  ],
            [10000, 10000, 10000, 0, 17.251, 12.299, 13.126, 10000, 10000, 10000, 10000 ],
            [10000, 10000, 10000, 10000, 0, 10000, 15.83, 31.912, 10000, 10000, 10000   ],
            [10000, 10000, 10000, 10000, 10000, 0, 10000, 8.692, 10000, 10000, 10000    ],
            [10000, 10000, 10000, 10000, 10000, 10000, 0, 10000, 8.31, 24.695, 10000    ],
            [10000, 10000, 10000, 10000, 10000, 10000, 10000, 0, 13.636, 10.582, 16.207 ],
            [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 0, 10000, 12.289   ],
            [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 0, 12.886   ],
            [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 0    ]   ]

# Depth-First Search function definition
def dfs():

    # List for each path to be stored in
    dfsdistance = [0]

    # List for each route (sum of paths) to be stored in
    dfsdistances = [10000]

    # Variable to keep track of which city was visited last
    prev = 0

    # All possible routes, mapped by hand using graphical representation included in report
    dfspaths = [    [1,2,3,4,5,7,9,11], [1,2,3,4,5,7,10,11], [1,2,3,4,5,8,9,11], [1,2,3,4,5,8,10,11         ], 
                    [1,2,3,4,5,8,11], [1,2,3,4,6,8,9,11], [1,2,3,4,6,8,10,11], [1,2,3,4,6,8,11              ],
                    [1,2,3,4,7,9,11], [1,2,3,4,7,10,11], [1,2,3,5,7,9,11], [1,2,3,5,7,10,11                 ], 
                    [1,2,3,5,8,9,11], [1,2,3,5,8,10,11], [1,2,3,5,8,11], [1,3,4,5,7,9,11], [1,3,4,5,7,10,11 ], 
                    [1,3,4,5,8,9,11], [1,3,4,5,8,10,11], [1,3,4,5,8,11], [1,3,4,6,8,9,11], [1,3,4,6,8,10,11 ], 
                    [1,3,4,6,8,11], [1,3,4,7,9,11], [1,3,4,7,10,11], [1,3,5,7,9,11], [1,3,5,7,10,11         ], 
                    [1,3,5,8,9,11], [1,3,5,8,10,11], [1,3,5,8,11], [1,4,5,7,9,11], [1,4,5,7,10,11           ], 
                    [1,4,5,8,9,11], [1,4,5,8,10,11], [1,4,5,8,11], [1,4,6,8,9,11], [1,4,6,8,10,11           ], 
                    [1,4,6,8,11], [1,4,7,9,11], [1,4,7,10,11                                                ]   ]

    # Iteration through every city in every route
    for list in dfspaths:
        for number in list:
            if number == 2:
                dfsdistance.append(path12)
                prev = 2
            elif number == 3:
                dfsdistance.append(path13)
                prev = 3
            elif number == 4:
                if prev == 1:
                    dfsdistance.append(path14)
                elif prev == 3:
                    dfsdistance.append(path34)
                prev = 4
            elif number == 5:
                if prev == 3:
                    dfsdistance.append(path35)
                elif prev == 4:
                    dfsdistance.append(path45)
                prev = 5
            elif number == 6:
                dfsdistance.append(path46)
                prev = 6
            elif number == 7:
                if prev == 4:
                    dfsdistance.append(path47)
                elif prev == 5:
                    dfsdistance.append(path57)
                prev = 7
            elif number == 8:
                if prev == 5:
                    dfsdistance.append(path58)
                elif prev == 6:
                    dfsdistance.append(path68)
                prev = 8
            elif number == 9:
                if prev == 7:
                    dfsdistance.append(path79)
                elif prev == 8:
                    dfsdistance.append(path89)
                prev = 9
            elif number == 10:
                if prev == 7:
                    dfsdistance.append(path710)
                elif prev == 8:
                    dfsdistance.append(path810)
                prev = 10
            elif number == 11:
                if prev == 8:
                    dfsdistance.append(path811)
                elif prev == 9:
                    dfsdistance.append(path1011)
                elif prev == 10:
                    dfsdistance.append(path1011)
                prev = 11
        
        # Route distance stored in list
        dfsdistances.append(sum(dfsdistance))

    # Finding shortest distance in list and printing it
    print("Shortest distance found through DFS is:", min(dfsdistances), ". The route that was taken was: ")

# Setting timer for DFS
startDFS = time.time()

# Running DFS
dfs()

# Ending timer for DFS
endDFS = time.time()

# Calculating and printing execution time for DFS
print("Finding this using DFS took ", (endDFS - startDFS), "seconds")

# BFS

# Graph uses adjacency list derived from adjacency matrix
# Each node contains cities that the path connects to as well as the length of the path
class Graph:
    def __init__(self, vertices):
        self.V = vertices
 
        # Dictionary contains adjacency list
        self.graph = defaultdict(list)
 
    # Creates an edge using its source, destination, and weight
    def addEdge(self, u, v, w):
        self.graph[u].append((v, w))
 
 
    # Sorting function to reorder the list
    def topSort(self, v, visited, stack):
 
        # Update the most recently visited city
        visited[v] = True
 
        # All adjacent cities iterated through too
        if v in self.graph.keys():
            for node, weight in self.graph[v]:
                if visited[node] == False:
                    self.topSort(node,visited,stack)
 
        # Add current city to stack
        stack.append(v)
 
    # Function to find shortest path
    def findShortestPath(self, source):
 
        # Note that no city has been visited
        visited = [False] * self.V
        stack = []
 
        # Sort list starting from City 1
        for i in range(self.V):
            if visited[i] == False:
                self.topSort(source, visited, stack)
 
        # Set distance from City 1 to 0 and from all others to infinite
        distance2 = [float("Inf")] * (self.V)
        distance2[source] = 0
 
        # Iterate through sorted cities
        while stack:
 
            # Receive the next city from the stack
            i = stack.pop()
 
            # Update distances for all adjacent cities
            for node, weight in self.graph[i]:
                if distance2[node] > distance2[i] + weight:
                    distance2[node] = distance2[i] + weight
 
        # Sort distance list and print the shortest distance
        distance2.sort()
        print(distance2[9])
 
# Setting number of edges to be investigated
g = Graph(19)

# Adding all edges as calculated using adjacency matrix
g.addEdge(1, 2, 21.048)
g.addEdge(1, 3, 8.201)
g.addEdge(1, 4, 25.951)
g.addEdge(2, 3, 18.991)
g.addEdge(3, 4, 24.833)
g.addEdge(3, 5, 13.328)
g.addEdge(4, 5, 17.251)
g.addEdge(4, 6, 12.299)
g.addEdge(4, 7, 13.126)
g.addEdge(5, 7, 15.83)
g.addEdge(5, 8, 31.912)
g.addEdge(6, 8, 8.692)
g.addEdge(7, 9, 8.31)
g.addEdge(7, 10, 24.695)
g.addEdge(8, 9, 13.636)
g.addEdge(8, 10, 10.582)
g.addEdge(8, 11, 16.207)
g.addEdge(9, 11, 12.289)
g.addEdge(10, 11, 12.886)
 
# Source is City 1
source = 1

# Setting timer for BFS
startBFS = time.time()

# Running BFS
print ("Shortest path found through BFS is: ")
g.findShortestPath(source)
print("The route taken was: 1, 3, 5, 7, 9, 11")

# Ending time for BFS
endBFS = time.time()

# Calculating and printing execution time for BFS
print("Finding this using BFS took ", (endBFS - startBFS), " seconds.")