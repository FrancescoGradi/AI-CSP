import mapColoring as mp
import random
from timeit import default_timer as timer

# La funzione restituisce un grafo che replica la mappa dell'Australia, l'algoritmo min-conflicts assegna colori casuali
# (in questo caso ne bastano 3) per ottenere regioni confinanti colorate in modo diverso

'''

map = mp.getAustraliaMap()

start = timer()
solution = mp.minConflicts(map, 10000)
end = timer()

if solution is 0:
    print "Solution not found in " + str(end - start) + " seconds"
else:
    print
    print "I found a solution in " + str(end - start) + " seconds and " + str(solution[1]) + " with " + \
        str(len(map.domains)) + " colors"
    for i in range(len(solution[0].regions)):
        print solution[0].regions[i].name + ": " + str(solution[0].regions[i].color)

    map.drawBiggerNodesMap()

'''

# In questo caso si ottiene un grafo casuale di n nodi con nColors, generato in modo che gli archi non si intersechino
# tramite l'algoritmo di Delaunay. In questo esempio il numero di colori parte da

n = 512
nColors = 2
steps = 100000

map = mp.getRandomMap(n, nColors)

while True:

    start = timer()
    solution = mp.minConflicts(map, steps)
    end = timer()

    if solution is 0:
        print "Solution not found in " + str(end - start) + " seconds and " + str(steps) + " with " + \
              str(len(map.domains)) + " colors"
        map.domains.append('#' + "%06x" % random.randint(0, 0xFFFFFF))
    else:
        print
        print "I found a solution in " + str(end - start) + " seconds and " + str(solution[1]) + " with " + \
              str(len(map.domains)) + " colors"
        map.drawMap()
        break
