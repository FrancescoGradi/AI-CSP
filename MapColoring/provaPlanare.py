from scipy.spatial import Delaunay
import networkx as nx
import random
# nodes and positions

n = 100
nodes = list()
points = list()

for i in range(n):
    nodes.append("R" + str(i))
    points.append((random.random() * 100, random.random() * 100))


t = Delaunay(points)
edges = []
m = dict(enumerate(nodes)) # mapping from vertices to nodes
for i in range(t.nsimplex):
    edges.append( (m[t.vertices[i,0]], m[t.vertices[i,1]]) )
    edges.append( (m[t.vertices[i,1]], m[t.vertices[i,2]]) )
    edges.append( (m[t.vertices[i,2]], m[t.vertices[i,0]]) )
print edges

for i in range(len(edges)):
    print edges[i][0]

# build graph
G = nx.Graph(edges)
pos = dict(zip(nodes,points))
# draw
import matplotlib.pyplot as plt
nx.draw(G,pos)
plt.show()

