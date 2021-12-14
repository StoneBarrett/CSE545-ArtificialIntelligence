# Stone Barrett
# CSE 545 Artificial Intelligence
# Project 1

# Importing helpful tools
import time
import numpy
from itertools import chain, permutations
import os

# Method to read file from current directory
def read_file(filepath):
    with open(filepath, 'r') as f:
        x = f.readlines()
# Create array using data from line 8 to end of the file
    points1 = x[7:] 
    points2 = []
    index = 0
    for index in range(0, len(points1)):
        firstWord, secondWord, thirdWord, *otherWords = points1[index].split()
        points2.append([])
        points2[index].append(float(secondWord))
        points2[index].append(float(thirdWord))
# Creating array with just coordinate points
    points3 = numpy.asarray(points2)
    return points3

# Method to add point of origin to beginning and end of each path
def finishHamiltonian(value1, iterator, value2):
    return chain([value1], iterator, [value2])

# Method to create permutations
def permuCreation(values):
    paths = list(permutations(range(1, len(values))))
    i = 0
    for i in range(0, len(paths)):
        paths[i] = list(paths[i])
        print(paths[i])
        paths[i] = list(finishHamiltonian(0, paths[i], 0))
    return paths

# Method for calculating distance between points
def distanceFormula(index1, index2):
    return (((numpy.sum(numpy.power(points3[index1] - points3[index2], 2))) ** 0.5))

# Method to sum distances in a given path
def sumOfPath(indexList):
    sum = 0.0
    for i in range(1, len(indexList)):
        sum += distanceFormula(indexList[i], indexList[i - 1])
    return sum

# Method to create array with all distances
def listances(paths):
    dist = []
    for i in range(0, len(paths)):
        dist.append([])
        dist[i] = (sumOfPath(paths[i]))
    return dist

# Method to compare all distances
def pathCompare(distance):
    temp_dis = float("inf")
    for i in range(0, len(distance) - 1):
        if distance[i] <= distance[i + 1] and distance[i] < temp_dis:
            temp_dis = distance[i]
        elif distance[i + 1] < temp_dis:
            temp_dis = distance[i + 1]
        else:
            continue
    return float(round(temp_dis, 2))

# Method to determine shortest path
def pathOptimal(distanceShort, distance, paths):
    pathShort = []
    for i in range(0, len(distance)):
        if distanceShort == float(round(distance[i], 2)):
            pathShort.append(paths[i])
        else:
            continue
    pathShort = numpy.array(pathShort)
    return pathShort + 1

# Reading file
points3 = read_file("Random11TESTP4.tsp")

# Running permutations
paths = permuCreation(points3)

# Clear terminal on Windows
os.system('cls' if os.name == 'nt' else 'clear')

print("\n----------------------------------------------------------------\n")
# Calculate and display all distances
listancesFinal = listances(paths)
print("\nAll distances: \n" + str(listancesFinal))

# Calculate and display shortest distance
smallestDistance = pathCompare(listancesFinal)
print("\nShortest distance: " + str(smallestDistance))

# Calculate and display optimal path
pathBest = pathOptimal(smallestDistance, listancesFinal, paths)
print("\nBest path(s): \n" + str(pathBest))

# Calculate and display runtime
print("\nRuntime: " + str(time.process_time()) + " seconds." )

print("\n----------------------------------------------------------------\n")