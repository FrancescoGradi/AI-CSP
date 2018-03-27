import random
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

class Problem:

    def __init__(self, n):
        # x rappresenta l'indice di colonna, tutte le righe sono diverse per definizione

        self.n = n
        self.x = range(n)

        # Questa e' una soluzione
        # self.x = [1, 3, 0, 2]

        # rappresentazione matriciale del problema, 1 corrisponde a una Queen

        self.matrix = np.zeros((len(self.x), len(self.x)))
        for i in range(len(self.x)):
            self.matrix[i][self.x[i]] = 1

    def getMatrix(self):
        self.matrix = np.zeros((len(self.x), len(self.x)))

        for i in range(len(self.x)):
            self.matrix[i][self.x[i]] = 1

        return self.matrix

    def setRandomX(self):
        for i in range(len(self.x)):
            self.x[i] = random.randint(0, len(self.x) - 1)

    def setX(self, current):
        for i in range(len(self.x)):
            self.x[i] = current[i]

    def drawQueens(self):
        matrix = np.zeros((n, n))
        matrix = matrix.astype(str)

        for i in range(n):
            for j in range(n):
                if self.x[i] == j:
                    matrix[i][j] = 'Q'
                else:
                    matrix[i][j] = ' '

        w = 5
        h = 5
        plt.figure(1, figsize=(w, h))
        tb = plt.table(cellText=matrix, loc=(0, 0), cellLoc='center')

        for i in range(n):
            for j in range(n):
                if self.x[i] == j:
                    tb._cells[(i, j)]._text.set_color('#960018')
                    tb._cells[(i, j)]._text.set_weight('extra bold')
                if ((i + j) % 2) == 0:
                    tb._cells[(i, j)].set_facecolor("#CD853F")
                else:
                    tb._cells[(i, j)].set_facecolor("#FADFAD")


        tc = tb.properties()['child_artists']
        for cell in tc:
            cell.set_height(1.0 / n)
            cell.set_width(1.0 / n)

        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])

        plt.show()


def minConflicts(problem, maxSteps):
    current = problem.x
    for i in range(maxSteps):
        if isSolution(current):
            return current, i
        var = chooseVar(current)
        value = conflicts(current, var)
        current[var] = value

    return 0


def minConflictsRandomRestart(problem, maxSteps, maxRestarts, count=0):
    current = problem.x

    for i in range(maxSteps):
        if isSolution(current):
            return current, i, count
        var = chooseVar(current)
        value = conflicts(current, var)
        current[var] = value

    if count < maxRestarts:
        count += 1
        problem.setRandomX()
        return minConflictsRandomRestart(problem, maxSteps, maxRestarts, count)

    return 0


# Min conflicts accettando mosse svantaggiose all'inizio con probabilita' piu' alta, via via a decrescere

def minConflictsSimulatedAnnealing(problem, maxSteps, temperature):
    current = problem.x
    for i in range(maxSteps):
        if isSolution(current):
            return current, i
        var = chooseVar(current)

        if random.randint(0, (temperature + i)) == 0:
            value = random.randint(0, len(current) - 1)
        else:
            value = conflicts(current, var)

        current[var] = value

    return 0


def isSolution(problem):
    # Dobbiamo verificare che tutte le colonne siano diverse, abbiano indici diversi
    # Per avere colonne tutte diverse non deve mai entrare nell'if

    # Verifica veloce per risparmiare tempo: se la somma degli indici di colonna e' diversa da n*(n+1)/2, dalla formula
    # di Gauss, allora non e' soluzione, altrimenti verifica

    n = len(problem) - 1

    if sum(problem) != (n * (n + 1) / 2):
        return False

    for i in range(len(problem)):
        tmp = problem[i]
        for j in range(i + 1, len(problem)):
            if tmp is problem[j]:
                return False

    # Adesso dobbiamo fare il test sulle diagonali, prima ritrasformo il problema in matrice

    matrix = np.zeros((len(problem), len(problem)))
    for i in range(len(problem)):
        matrix[i][problem[i]] = 1

    # Analizzo ciascuna diagonale primaria e guardo che non ci siano due 1 in una diagonale

    for k in range((len(matrix[0]) * 2) - 1):
        diagonal = np.diagonal(matrix, k - (len(matrix[0]) - 1))
        if sum(diagonal) > 1:
            return False

    # Analizzo ciascuna antidiagonale e guardo che non ci siano due 1 in una diagonale

    matrix = np.fliplr(matrix)

    for k in range((len(matrix[0]) * 2) - 1):
        antidiagonal = np.diagonal(matrix, k - (len(matrix[0]) - 1))
        if sum(antidiagonal) > 1:
            return False

    return True


def chooseVar(current):
    # Var e' scelta in modo casuale, rappresenta il suo indice

    return random.randint(0, len(current) - 1)


def conflicts(current, var):
    # Data la lista delle variabili e quella da controllare, devo guardare il numero di conflitti per ogni assegnazione
    # eseguibile, in questo caso posso spostare le regine soltanto in orizzontale, scegliendo l'assegnazione di colonna
    # che provoca il minor numero di conflitti

    conflictsList = np.zeros(len(current))

    matrix = np.zeros((len(current), len(current)))
    for i in range(len(current)):
        matrix[i][current[i]] = 1

    for j in range(len(conflictsList)):

        count = 0
        count += countRowsConflicts(matrix, j, current, var)
        count += countDiagonalConflicts(matrix, j, current, var)

        # Se sto verificando un elemento che e' gia' assegnato, diagonale e antidiagonale l'hanno contato una volta in
        # piu'

        if j is current[var]:
            count -= 2

        conflictsList[j] = count

    # Una volta creata la lista dei conflitti, trovo il valore minimo dei conflitti e creo una lista contenente gli
    # indici delle assegnazioni migliori. Scelgo a caso un'assegnazione tra di esse, per non incappare in un plateaux

    minValue = int(np.min(conflictsList))
    minima = list()

    for j in range(len(conflictsList)):
        if conflictsList[j] == minValue:
            minima.append(j)

    return minima[random.randint(0, len(minima) - 1)]


def countRowsConflicts(matrix, j, current, var):
    count = 0
    for i in range(len(matrix[0])):
        if matrix[i][j] and j is not current[var] and i is not var:
            count += 1

    return count


def countDiagonalConflicts(matrix, j, current, var):
    count = 0

    diagonal = np.diagonal(matrix, j - var)
    for k in range(len(diagonal)):
        if diagonal[k] == 1:
            count += 1

    flippedMatrix = np.fliplr(matrix)
    antidiagonal = np.diagonal(flippedMatrix, len(current) - var - j - 1)
    for k in range(len(antidiagonal)):
        if antidiagonal[k]:
            count += 1

    return count


n = 128
p = Problem(n)
p.setRandomX()
#p.drawQueens()

print "Initial random assignment: "
print
print p.x

print

print "Running MinConflicts heuristic: "

print

# Min Conflicts

'''
steps = 100000
current = minConflicts(p, steps)

if current is 0:
    print "Solution not found in " + str(steps) + " steps"
else:
    print "I found a solution in " + str(current[1]) + " steps"
    print
    print p.getMatrix()

    p.drawQueens()
'''

# Min Conflicts using Random Restart

'''
steps = 10000
restarts = 15

start = timer()

current = minConflictsRandomRestart(p, steps, restarts)

end = timer()

print sum(current[0])

if current is 0:
    print "Solution not found in " + str(steps) + " steps, " + str(end - start) + " seconds and " + str(restarts) + " random restarts"
else:
    print "I found a solution in " + str(current[1]) + " steps, " + str(end - start) + " seconds and " + str(current[2]) + " random restarts"
    print
    print p.getMatrix()

    #p.drawQueens()


# Min Conflicts using Simulated Annealing

'''
steps = 100000
temperature = 5

start = timer()

current = minConflictsSimulatedAnnealing(p, steps, temperature)

end = timer()

if current is 0:
    print "Solution not found in " + str(steps) + " steps, " + str(end - start) + " seconds"
else:
    print "I found a solution in " + str(current[1]) + " steps, " + str(end - start) + " seconds"
    print
    print p.getMatrix()

    #p.drawQueens()

