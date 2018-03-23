import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import planarity

class Map:
    def __init__(self):
        self.regions = list()
        self.domains = list()

    def drawMap(self):
        g = nx.Graph()
        colors = list()
        pos = dict()
        for region in self.regions:
            colors.append(region.color)
            pos[region.name] = [region.posX, region.posY]
            if len(region.neighbors) == 0:
                g.add_edge(region.name, region.name)
            for neighbor in region.neighbors:
                g.add_edge(region.name, neighbor.name)

        nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=1000)
        nx.draw_networkx_labels(g, pos, font_size=14)
        nx.draw_networkx_edges(g, pos)

        print planarity.is_planar(g)

        plt.show()


class Region:
    def __init__(self, name=None, color=None, posX=0.0, posY=0.0):
        self.color = color
        self.name = name
        self.neighbors = list()
        self.posX = posX
        self.posY = posY

    def setName(self, name):
        self.name = name

    def setColor(self, color):
        self.color = color


def getAustraliaMap():

    map = Map()
    for i in range(3):
        map.domains.append('#' + "%06x" % random.randint(0, 0xFFFFFF))

    T = Region('T', posX=1.8, posY=-2.2)
    NT = Region('NT', posX=-0.2, posY=1)
    WA = Region('WA', posX=-2, posY=0.4)
    SA = Region('SA', posX=0, posY=0)
    Q = Region('Q', posX=1.9, posY=0.7)
    NSW = Region('NSW', posX=2.1, posY=0)
    V = Region('V', posX=1.6, posY=-1)

    NT.neighbors.append(WA)
    NT.neighbors.append(SA)
    NT.neighbors.append(Q)
    WA.neighbors.append(NT)
    WA.neighbors.append(SA)
    SA.neighbors.append(WA)
    SA.neighbors.append(NT)
    SA.neighbors.append(V)
    SA.neighbors.append(Q)
    SA.neighbors.append(NSW)
    Q.neighbors.append(NT)
    Q.neighbors.append(SA)
    Q.neighbors.append(NSW)
    NSW.neighbors.append(V)
    NSW.neighbors.append(Q)
    NSW.neighbors.append(SA)
    V.neighbors.append(SA)
    V.neighbors.append(NSW)
    V.neighbors.append(NT)
    NT.neighbors.append(V)

    map.regions.append(WA)
    map.regions.append(Q)
    map.regions.append(T)
    map.regions.append(V)
    map.regions.append(SA)
    map.regions.append(NT)
    map.regions.append(NSW)

    return map

def getRandomMap(n):

    map = Map()
    for i in range(n):
        map.domains.append('#' + "%06x" % random.randint(0, 0xFFFFFF))

    # Inserisco n nodi a caso dentro la mappa
    for i in range(n):
        map.regions.append(Region("R" + str(i), posX=float(random.random()), posY=float(random.random())))

    #for i in range(n):
    #   map.regions.neighbors.append(map.regions(random.randint(0, len(map.regions) - 1)))

    return map

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

map = getRandomMap(100)
randomAssignment(map)
map.drawMap()

map = getAustraliaMap()

solution = minConflicts(map, 10000)

if solution is 0:
    print "Solution not found"
else:
    for i in range(len(solution[0].regions)):
        print solution[0].regions[i].name + ": " + solution[0].regions[i].color

    map.drawMap()

