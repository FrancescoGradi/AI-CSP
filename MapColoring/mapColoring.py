import random
import matplotlib as plt
import networkx as nx
import numpy as np

class Map:
    def __init__(self):
        self.regions = list()
        self.domains = None

class Region:
    def __init__(self, name=None, color=None):
        self.color = color
        self.name = name
        self.neighbors = list()

    def setName(self, name):
        self.name = name

    def setColor(self, color):
        self.color = color


def getAustraliaMap():

    map = Map()
    map.domains = ['RED', 'GREEN', 'BLUE']

    T = Region('T')
    NT = Region('NT')
    WA = Region('WA')
    SA = Region('SA')
    Q = Region('Q')
    NSW = Region('NSW')
    V = Region('V')

    NT.neighbors.append(WA)
    NT.neighbors.append(SA)
    NT.neighbors.append(Q)
    WA.neighbors.append(NT)
    WA.neighbors.append(SA)
    SA.neighbors.append(WA)
    SA.neighbors.append(NT)
    SA.neighbors.append(V)
    SA.neighbors.append(Q)
    Q.neighbors.append(NT)
    Q.neighbors.append(SA)
    Q.neighbors.append(NSW)
    NSW.neighbors.append(V)
    NSW.neighbors.append(Q)
    V.neighbors.append(SA)
    V.neighbors.append(NSW)

    map.regions.append(T)
    map.regions.append(NT)
    map.regions.append(WA)
    map.regions.append(SA)
    map.regions.append(Q)
    map.regions.append(NSW)
    map.regions.append(V)

    return map

map = getAustraliaMap()

def minConflicts(problem, maxSteps):
    current = problem
    randomAssignment(current)

    for i in range(maxSteps):
        if isSolution(current):
            return current, i
        var = chooseVar(current)
        value = conflicts(current, var)
        var.color = problem.domains[value]

    return 0


def randomAssignment(current):
    for i in range(len(current.regions)):
        current.regions[i].color = current.domains[random.randint(0, len(current.domains) - 1)]


def isSolution(current):
    for i in range(len(current.regions)):
        for j in range(len(current.regions[i].neighbors)):
            if current.regions[i].color == current.regions[i].neighbors[j].color:
                return False

    return True


def chooseVar(current):
    return current.regions[random.randint(0, len(current.regions) - 1)]


def conflicts(current, var):
    colorConflict = np.zeros(len(current.domains))
    for i in range(len(current.domains)):
        count = 0
        for j in range(len(var.neighbors)):
            if current.domains[i] == var.neighbors[j].color:
                count += 1
        colorConflict[i] = count

    minColorConflict = int(np.min(colorConflict))
    minima = list()

    for k in range(len(colorConflict)):
        if colorConflict[k] == minColorConflict:
            minima.append(k)

    return minima[random.randint(0, len(minima) - 1)]

map = getAustraliaMap()

solution = minConflicts(map, 10000)

for i in range(len(solution[0].regions)):
    print solution[0].regions[i].name + ": " + solution[0].regions[i].color

