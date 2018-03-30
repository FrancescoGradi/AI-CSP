import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pylab as pl
from scipy.spatial import Delaunay

class Map:
    def __init__(self):
        self.regions = list()
        self.domains = list()

    def drawMap(self):
        g = nx.Graph()
        colorsRegions = list()
        pos = dict()
        for region in self.regions:
            colorsRegions.append((region.name, region.color))
            pos[region.name] = [region.posX, region.posY]
            if len(region.neighbors) == 0:
                g.add_edge(region.name, region.name)
            for neighbor in region.neighbors:
                g.add_edge(region.name, neighbor.name)

        colors = list()
        for node in g.nodes:
            for i in range(len(g.nodes)):
                if node is colorsRegions[i][0]:
                    colors.append(colorsRegions[i][1])

        nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=100)
        nx.draw_networkx_labels(g, pos, font_size=2)
        nx.draw_networkx_edges(g, pos)

        plt.show()

    def drawBiggerNodesMap(self):
        g = nx.Graph()
        colorsRegions = list()
        pos = dict()
        for region in self.regions:
            colorsRegions.append((region.name, region.color))
            pos[region.name] = [region.posX, region.posY]
            if len(region.neighbors) == 0:
                g.add_edge(region.name, region.name)
            for neighbor in region.neighbors:
                g.add_edge(region.name, neighbor.name)

        colors = list()
        for node in g.nodes:
            for i in range(len(g.nodes)):
                if node is colorsRegions[i][0]:
                    colors.append(colorsRegions[i][1])

        nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=1000)
        nx.draw_networkx_labels(g, pos, font_size=14)
        nx.draw_networkx_edges(g, pos)

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
    # Funzione che genera un grafo che replica la mappa dell'Australia, dall'esempio del Russell-Norvig

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

    map.regions.append(WA)
    map.regions.append(Q)
    map.regions.append(T)
    map.regions.append(V)
    map.regions.append(SA)
    map.regions.append(NT)
    map.regions.append(NSW)

    return map

def getRandomMap(n, nDomains):
    map = Map()
    for i in range(nDomains):
        map.domains.append('#' + "%06x" % random.randint(0, 0xFFFFFF))

    # Inserisco n nodi a caso dentro la mappa
    points = list()
    nodes = list()
    for i in range(n):
        map.regions.append(Region("R" + str(i), posX=float(random.random()), posY=float(random.random())))
        points.append((map.regions[i].posX, map.regions[i].posY))
        nodes.append(map.regions[i])

    # Applico algoritmo di Delaunay per assegnare archi che non si intersechino fra loro, resistuisce una lista
    # di archi che rispetta questa proprieta', puo' essere usata quindi per generare archi casuali

    t = Delaunay(points)
    edges = []
    m = dict(enumerate(nodes))

    for i in range(t.nsimplex):
        edges.append((m[t.vertices[i, 0]], m[t.vertices[i, 1]]))
        edges.append((m[t.vertices[i, 1]], m[t.vertices[i, 2]]))
        edges.append((m[t.vertices[i, 2]], m[t.vertices[i, 0]]))

    for i in range(len(edges)):
        if edges[i][1] not in edges[i][0].neighbors:
            edges[i][0].neighbors.append(edges[i][1])
        if edges[i][0] not in edges[i][1].neighbors:
            edges[i][1].neighbors.append(edges[i][0])

    return map

def minConflicts(problem, maxSteps):
    randomAssignment(problem)

    for i in range(maxSteps):
        if isSolution(problem):
            return problem, i
        var = chooseVar(problem)
        value = conflicts(problem, var)
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