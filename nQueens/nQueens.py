import random
import numpy as np
import matplotlib.pyplot as plt

class Problem:

    def __init__(self, n):
        # x[i] rappresenta l'indice di colonna, tutte le righe sono diverse per definizione

        self.n = n
        self.x = range(n)

        # Questa e' una soluzione per n = 4
        # self.x = [1, 3, 0, 2]

        # rappresentazione matriciale del problema, 1 corrisponde a una Queen

        self.matrix = np.zeros((len(self.x), len(self.x)))
        for i in range(len(self.x)):
            self.matrix[i][self.x[i]] = 1

    def getMatrix(self):
        return self.matrix

    def setRandomX(self):
        for i in range(len(self.x)):
            tmp = self.x[i]
            self.x[i] = random.randint(0, len(self.x) - 1)
            self.matrix[i][tmp] = 0
            self.matrix[i][self.x[i]] = 1

    def setMinConflictsRandomX(self):
        # Assegno il primo valore casualmente
        self.matrix = np.zeros((len(self.x), len(self.x)))
        self.x[0] = random.randint(0, len(self.x) - 1)
        self.matrix[0][self.x[0]] = 1

        for i in range(1, len(self.x)):
            # None valore di Default per le variabili non ancora assegnate, quindi non creano conflitti, corrispondono
            # a zeri nella matrice

            self.x[i] = None

            value = self.initialConflicts(i)
            self.x[i] = value
            self.matrix[i][value] = 1

    def initialConflicts(self, i):
        conflictsList = np.zeros(len(self.x))

        for j in range(len(conflictsList)):

            count = 0
            count += countRowsConflicts(self.matrix, j, self.x, i)
            count += countDiagonalConflicts(self.matrix, j, self.x, i)

            conflictsList[j] = count

        minValue = int(np.min(conflictsList))
        minima = list()

        for j in range(len(conflictsList)):
            if conflictsList[j] == minValue:
                minima.append(j)

        return minima[random.randint(0, len(minima) - 1)]


    def setX(self, x):
        for i in range(self.n):
            tmp = self.x[i]
            self.x[i] = x[i]
            self.matrix[i][tmp] = 0
            self.matrix[i][self.x[i]] = 1

    def drawQueens(self):
        matrix = np.zeros((self.n, self.n))
        matrix = matrix.astype(str)

        for i in range(self.n):
            for j in range(self.n):
                if self.x[i] == j:
                    matrix[i][j] = 'Q'
                else:
                    matrix[i][j] = ' '

        w = 5
        h = 5
        plt.figure(1, figsize=(w, h))
        tb = plt.table(cellText=matrix, loc=(0, 0), cellLoc='center')

        for i in range(self.n):
            for j in range(self.n):
                if self.x[i] == j:
                    tb._cells[(i, j)]._text.set_color('#960018')
                    tb._cells[(i, j)]._text.set_weight('extra bold')
                if ((i + j) % 2) == 0:
                    tb._cells[(i, j)].set_facecolor("#CD853F")
                else:
                    tb._cells[(i, j)].set_facecolor("#FADFAD")


        tc = tb.properties()['child_artists']
        for cell in tc:
            cell.set_height(1.0 / self.n)
            cell.set_width(1.0 / self.n)

        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])

        plt.show()


def minConflicts(problem, maxSteps):
    for i in range(maxSteps):
        if isSolution(problem):
            return problem.x, i
        var = chooseVar(problem.x)
        value = conflicts(problem, var)
        tmp = problem.x[var]
        problem.x[var] = value
        problem.matrix[var][tmp] = 0
        problem.matrix[var][value] = 1

    return 0


def minConflictsRandomRestart(problem, maxSteps, maxRestarts, count=0):
    for i in range(maxSteps):
        if isSolution(problem):
            return problem.x, i, count
        var = chooseVar(problem.x)
        value = conflicts(problem, var)
        tmp = problem.x[var]
        problem.x[var] = value
        problem.matrix[var][tmp] = 0
        problem.matrix[var][value] = 1

    if count < maxRestarts:
        count += 1
        problem.setRandomX()
        return minConflictsRandomRestart(problem, maxSteps, maxRestarts, count)

    return 0

def isSolution(problem):
    # Dobbiamo verificare che tutte le colonne siano diverse, abbiano indici diversi
    # Per avere colonne tutte diverse non deve mai entrare nell'if

    # Verifica veloce per risparmiare tempo: se la somma degli indici di colonna e' diversa da n*(n+1)/2, dalla formula
    # di Gauss, allora non e' soluzione, altrimenti verifica

    n = len(problem.x) - 1

    if sum(problem.x) != (n * (n + 1) / 2):
        return False

    for i in range(len(problem.x)):
        tmp = problem.x[i]
        for j in range(i + 1, len(problem.x)):
            if tmp is problem.x[j]:
                return False

    # Analizzo ciascuna diagonale primaria e guardo che non ci siano due 1 in una diagonale

    for k in range((len(problem.matrix[0]) * 2) - 1):
        diagonal = np.diagonal(problem.matrix, k - (len(problem.matrix[0]) - 1))
        if sum(diagonal) > 1:
            return False

    # Analizzo ciascuna antidiagonale e guardo che non ci siano due 1 in una diagonale

    flipMatrix = np.fliplr(problem.matrix)

    for k in range((len(flipMatrix[0]) * 2) - 1):
        antidiagonal = np.diagonal(flipMatrix, k - (len(flipMatrix[0]) - 1))
        if sum(antidiagonal) > 1:
            return False

    return True


def chooseVar(current):
    # Var e' scelta in modo casuale, rappresenta il suo indice

    return random.randint(0, len(current) - 1)


def conflicts(problem, var):
    # Data la lista delle variabili e quella da controllare, devo guardare il numero di conflitti per ogni assegnazione
    # eseguibile, in questo caso posso spostare le regine soltanto in orizzontale, scegliendo l'assegnazione di colonna
    # che provoca il minor numero di conflitti

    conflictsList = np.zeros(len(problem.x))

    for j in range(len(conflictsList)):

        count = 0
        count += countRowsConflicts(problem.matrix, j, problem.x, var)
        count += countDiagonalConflicts(problem.matrix, j, problem.x, var)

        # Se sto verificando un elemento che e' gia' assegnato, diagonale e antidiagonale l'hanno contato una volta in
        # piu'

        if j is problem.x[var]:
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