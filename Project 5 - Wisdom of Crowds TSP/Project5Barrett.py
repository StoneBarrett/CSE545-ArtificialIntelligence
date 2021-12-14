# Stone Barrett
# CSE 545 Artificial Intelligence
# Project 5

# Importing helpful tools
import matplotlib.pyplot
import numpy
import operator
import pandas
from pathlib import Path
import random
import time

# City class
class City:
    def __init__(self, x, y):
        self.location = numpy.array([x,y], dtype = float)
    
    def distance(self, otherCity):
        distance = numpy.sqrt(((abs(self.location[0] - otherCity.location[0])) ** 2) + ((abs(self.location[1] - otherCity.location[1])) ** 2))
        return distance
    
# Edge class
class Edge:
    def __init__(self, cfrom, cto):
        self.cfrom = cfrom.location
        self.cto = cto.location

# Individual population member class
class Individual:
    def __init__(self, cityList):
        self.route = cityList
        self.fitness = 0
    
    def indivCost(self):
        if self.fitness == 0: # May not need, test later
            
            # Temp variable to hold value while summing route length
            temp = 0
            
            # Iterating route
            for i in range(0, len(self.route)):
                current = self.route[i]
                next = None
                
                # Checking if any more unvisited cities
                if i + 1 < len(self.route):
                    next = self.route[i + 1]
                
                # Completing Hamiltonian cycle
                else:
                    next = self.route[0]
                
                # Adding the traversed edge
                temp += current.distance(next)
            
            # Total route sum is cost of this individual
            self.fitness = temp
        return self.fitness
    
    # Find fitness function
    def indivFitness(self):
        if self.fitness == 0:

            # Fitness is inverse of cost
            self.fitness = 1 / float(self.indivCost())
        return self.fitness

# Read file from current directory
def readFile(filepath):
    p = Path(__file__).with_name(filepath)

    # Create list with every line in file
    with p.open('r') as f:
        everyLine = f.readlines()

    # Create new list leaving out irrelevant information
    relevantLines = everyLine[7:]

    # Create list of city objects
    cities = [City(0, 0) for _ in range(0, len(relevantLines))]
    for i in range(0, len(relevantLines)):
        index, x, y = relevantLines[i].split()
        cities[i].location = numpy.array([x,y], dtype = float)
    
    return cities

# Create random routes for Generation 0
def randomRoute(cities):
    route = random.sample(cities, len(cities))
    return route

# Create Generation 0
def gen0(populationSize, cities):
    population = []
    # By adding random routes generated in the amount of desired population size
    for i in range(0, populationSize):
        population.append(randomRoute(cities))
    return population

# Determining fitness of each route in a population
def darwinScore(population):
    fitnessResults = {}
    for i in range(0, len(population)):
        fitnessResults[i] = Individual(population[i]).indivFitness()
    # Set is ordered reverse since inverse of cost is fitness, not cost
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

# Select which members of the population are fit to reproduce for best results
def selection(popRanked, eliteCount):
    selectionResults = []

    # Pandas library datafram allows easy handling of data
    # Assigning weighted likelihoods to individuals
    df = pandas.DataFrame(numpy.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    # Automatically select the number of desired elites to carry over
    for i in range(0, eliteCount):
        selectionResults.append(popRanked[i][0])

    # Using weighted RNG, fill remaining slots with population members
    # Individuals with higher fitness are more likely to be chosen
    for i in range(0, len(popRanked) - eliteCount):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

# Creating the mating pool based on selected individuals
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# First crossover method
# Takes random subsection of one parent to give to child
# Fills remaining "gene" slots with complement from other parent
# "Genes" are where in the route cities are visited
def crossover1(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)
    for i in range(startGene, endGene):
        childP1.append(parent1[i])
    
    # List comprehension fills remaining "chromosome" slots with complement from second parent
    childP2 = [item for item in parent2 if item not in childP1]
    child = childP1 + childP2
    return child

# Crossover method running throughout the selected mating pool
def breeding(matingpool, eliteCount):
    children = []

    # Accounting for slots already occupied by desired number of elites
    length = len(matingpool) - eliteCount
    pool = random.sample(matingpool, len(matingpool))
    for i in range(0, eliteCount):
        children.append(matingpool[i])
    
    # Breeding among the remaining individuals in the mating pool
    for i in range(0, length):
        child = crossover1(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children

# Mutation method
# This can work as x different mutation methods because the chance of it happening can be changed
# Given chance of happening, randomly selected cities are swapped in the route
def mutate(individual, mutationChance):
    for swapped in range(len(individual)):
        if(random.random() < mutationChance):

            # City is chosen at random to be swapped with
            swapWith = int(random.random() * len(individual))
            city1 = individual[swapped]
            city2 = individual[swapWith]
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

# Mutation method running throughout the population at the desired rate
def mutating(population, mutationChance):
    mutatedPop = []
    for i in range(0, len(population)):
        mutatedInd = mutate(population[i], mutationChance)
        mutatedPop.append(mutatedInd)
    return mutatedPop

# Creating subsequent generations
def nextGen(currentGen, eliteCount, mutationChance):

    # Rating fitness
    popRanked = darwinScore(currentGen)

    # Selecting members
    selectionResults = selection(popRanked, eliteCount)

    # Creating mating pool
    matingpool = matingPool(currentGen, selectionResults)

    # Breeding
    children = breeding(matingpool, eliteCount)

    # Mutating
    genI = mutating(children, mutationChance)
    return genI

# Visualization 
def showTour(visitedCities):
    xPointsTest = []
    for i in range(0, len(visitedCities)):
        xPointsTest.append(visitedCities[i].location[0])
    yPointsTest = []
    for i in range(0, len(visitedCities)):
        yPointsTest.append(visitedCities[i].location[1])
    
    # Bug fix: Hamiltonian cycle not completing, graphical issue only
    xPointsTest.append(visitedCities[0].location[0])
    yPointsTest.append(visitedCities[0].location[1])
    
    matplotlib.pyplot.plot(xPointsTest, yPointsTest, 'o')
    matplotlib.pyplot.plot(xPointsTest, yPointsTest)
    matplotlib.pyplot.show()

# Tying everything together
def geneticAlgorithm(population, populationCount, eliteCount, mutationChance, generations, run):
    test = 1

    # Creating initial generation
    pop = gen0(populationCount, population)

    # Displaying initial route and cost
    print("Initial distance: " + str(1 / darwinScore(pop)[0][1]))
    #showTour(pop[0])

    # Creating list of best costs throughout generations
    progress = []
    progress.append(1 / darwinScore(pop)[0][1])
    for i in range(0, generations):
        pop = nextGen(pop, eliteCount, mutationChance)
        progress.append(1 / darwinScore(pop)[0][1])

        # Progress indicator
        if test % 500 == 0:
            print("Generation: ", test)
        
        test += 1

    # Displaying final route and cost
    print("GA Run", run, "distance: " + str(1 / darwinScore(pop)[0][1]))

    # Visualization
    # matplotlib.pyplot.plot(progress)
    # matplotlib.pyplot.ylabel('Cost')
    # matplotlib.pyplot.xlabel('Generation')
    # matplotlib.pyplot.show()
    #showTour(pop[0])

    if run == 4:
        matplotlib.pyplot.plot(progress)
        matplotlib.pyplot.ylabel('Cost')
        matplotlib.pyplot.xlabel('Generation')
        matplotlib.pyplot.show()
        showTour(pop[0])

    return pop

# WOC attempt
def WOC(pop1, pop2, pop3, pop4):
    pops = [pop1, pop2, pop3, pop4]
    crowdMember1 = random.choice(pops)
    crowdMember2 = random.choice(pops)
    aggregate = []
    aggregate1 = []
    aggregate2 = []

    opinionA = int(random.random() * len(crowdMember1))
    opinionB = int(random.random() * len(crowdMember1))
    startOpinion = min(opinionA, opinionB)
    endOpinion = max(opinionA, opinionB)

    for i in range(startOpinion, endOpinion):
        aggregate1.append(crowdMember1[i])
    
    aggregate2 = [item for item in crowdMember2 if item not in aggregate1]
    aggregate = aggregate1 + aggregate2

    print("Consensus distance: " + str(1 / darwinScore(aggregate)[0][1]))
    showTour(aggregate[0])

# Reading city locations from provided dataset
cities = readFile("Random22.tsp")

# Timing
startTime = time.time()

# Running GA
run1 = geneticAlgorithm(cities, 200, 25, 0.001, 2500, 1)
run2 = geneticAlgorithm(cities, 200, 25, 0.001, 2500, 2)
run3 = geneticAlgorithm(cities, 200, 25, 0.001, 2500, 3)
run4 = geneticAlgorithm(cities, 200, 25, 0.001, 2500, 4)

# Running WOC
WOC(run1, run2, run3, run4)

endTime = time.time()
print("Completed in", endTime - startTime, "seconds.")