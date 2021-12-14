# Stone Barrett
# CSE 545 Artificial Intelligence
# Project 3

# Import helpful tools
import matplotlib.pyplot
import numpy
from pathlib import Path
import random

# Calculate distance between city and city
def city2city(c1, c2):
    return numpy.linalg.norm(c1 - c2)

# Calculate distance between city and edge
def city2edge(c1, e1, e2):
    return abs(numpy.cross(e2 - e1, c1 - e1)/numpy.linalg.norm(e2 - e1))

# City class
class City:
    def __init__(self, x, y):
        self.location = numpy.array([x,y], dtype = float)

# Edge class
class Edge:
    def __init__(self, cfrom, cto):
        self.length = city2city(cfrom.location, cto.location)
        self.cfrom = cfrom.location
        self.cto = cto.location

# Read file from current directory
def readFile(filepath):
    p = Path(__file__).with_name(filepath)

    # Create list with every line in file
    with p.open('r') as f:
        everyLine = f.readlines()
    
    # Create new list leaving out irrelevant lines
    relevantLines = everyLine[7:]
    
    # Delete old list 
    del(everyLine)

    # Create list of city objects 
    cities = [City(0, 0) for _ in range(0, len(relevantLines))]
    for i in range(0, len(relevantLines)):
        index, x, y = relevantLines[i].split()
        cities[i].location = numpy.array([x,y], dtype = float)
    
    # Delete old list
    del(relevantLines)

    return cities

# Uncomment which data set to use
cities = readFile('Random30.tsp')
#cities = readFile('Random40.tsp')

# Visualization 
def showTour(visitedCities):
    xPointsTest = []
    for i in range(0, len(visitedCities) - 1):
        xPointsTest.append(visitedCities[i].location[0])
    yPointsTest = []
    for i in range(0, len(visitedCities) - 1):
        yPointsTest.append(visitedCities[i].location[1])
    
    matplotlib.pyplot.plot(xPointsTest, yPointsTest, 'o')
    matplotlib.pyplot.plot(xPointsTest, yPointsTest)
    matplotlib.pyplot.show()
    
# Algorithm implementation
def closestEdgeHeuristic(cities):

    # Picking random starting cities
    randomIndex = random.randint(0, len(cities) - 1)
    randomIndex2 = random.randint(0, len(cities) - 1)

    # Random int to help handle edge cases
    randomIncOrDec = random.randint(1, 10)
    
    # Ensuring rolls are not the same city
    if randomIndex2 == randomIndex:
        if randomIncOrDec < 5:
            randomIndex2 = randomIndex2 - 1
        # Handling edge cases (an index of [-1] would roll over to the last element of the list, but element out of range needs correcting)
        elif randomIncOrDec > 5:
            if randomIndex2 == len(cities) - 1:
                randomIndex2 = randomIndex2 - 1
            else:
                randomIndex2 = randomIndex2 + 1
        
    # Starting tour
    # List for cities that are already in tour
    visitedCities = []
    
    # Adding first random city to visited list
    visitedCities.append(cities[randomIndex])
    # Removing from unvisited list
    cities.pop(randomIndex)

    # Adding second random city to visited list
    visitedCities.append(cities[randomIndex2])
    # Removing from unvisited list
    cities.pop(randomIndex2)
    
    # List for edges that are in tour
    edges = []
    edges.append(Edge(visitedCities[0], visitedCities[1]))

    # Algorithm
    currentDistance = 0
    bestDistance = 0

    # This block runs if 30 city dataset
    if len(cities) == 28:
        for i in range(0, 27):
            for j in range(0, 28):
                currentDistance = city2edge(cities[i].location, edges[j].cfrom, edges[j].cto)
                tmp = 0
                tmp2 = 0
                if bestDistance == 0 or bestDistance > currentDistance:
                    bestDistance = currentDistance
                    visitedCities.append(cities[i])
                    cities.pop(i)
                    #edges.append(Edge(visitedCities[i - 1], visitedCities[i]))
                    #edges[j - 1] = Edge(visitedCities[i - 1], visitedCities[i])
                    tmp = tmp + 1
                else:
                    tmp2 = tmp2 + 1
                if tmp > tmp2:
                    edges.append(Edge(visitedCities[i - 1], visitedCities[i]))

    # This block runs if 40 city dataset
    elif len(cities) == 38:
        for i in range(0, 37):
            for j in range(0, len(edges) - 1):
                currentDistance = city2edge(cities[i].location, edges[j].cfrom, edges[j].cto)
                if bestDistance == 0 or bestDistance > currentDistance:
                    bestDistance = currentDistance
                    visitedCities.append(cities[i])
                    cities.pop(i)
                    edges.append(Edge(visitedCities[i - 1], visitedCities[i]))
    
    # This block runs if other dataset
    else:
        for i in range(0, 37):
            for j in range(0, len(edges) - 1):
                currentDistance = city2edge(cities[i].location, edges[j].cfrom, edges[j].cto)
                if bestDistance == 0 or bestDistance > currentDistance:
                    bestDistance = currentDistance
                    visitedCities.append(cities[i])
                    cities.pop(i)
                    edges.append(Edge(visitedCities[i - 1], visitedCities[i]))

    # Finishing Hamiltonian
    visitedCities.append(visitedCities[0])
    edges.append(Edge(visitedCities[-1], visitedCities[0]))

    # Sum of edge lengths
    tourSum = 0
    for i in range(0, len(edges) - 1):
        tourSum = tourSum + edges[i].length
    
    print(tourSum)
    return visitedCities

# Running algorithm
#visitedCities = closestEdgeHeuristic(cities)

# Drawing
#showTour(visitedCities)

# Testing
# edges = [Edge(cities[20], cities[23])]
# currentDistance = city2edge(cities[10].location, edges[0].cfrom, edges[0].cto)
# print(currentDistance)
showTour(cities)