import nQueens as nq
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

n = [8, 16, 32, 64]
k = 20
steps = 10000

# Time test and step test in max 10000 steps

yTimeMin = list()
yTimeAvg = list()
yTimeMax = list()

yStepsMin = list()
yStepsAvg = list()
yStepsMax = list()

yNoSolutions = list()

for i in range(len(n)):
    yTimeTmp = list()
    yStepsTmp = list()
    yNoSolutions.append(0)

    for j in range(k):
        p = nq.Problem(n[i])

        p.setRandomX()

        start = timer()

        current = nq.minConflicts(p, steps)

        end = timer()

        yTimeTmp.append(end - start)

        if current is 0:
            yNoSolutions[i] += 1
            yStepsTmp.append(steps)
        else:
            yStepsTmp.append(current[1])

    yTimeMin.append(min(yTimeTmp))
    yTimeAvg.append(np.average(yTimeTmp))
    yTimeMax.append(max(yTimeTmp))

    yStepsMin.append(min(yStepsTmp))
    yStepsAvg.append(np.average(yStepsTmp))
    yStepsMax.append(max(yStepsTmp))

plt.plot(n, yTimeMin)
plt.plot(n, yTimeAvg)
plt.plot(n, yTimeMax)
plt.xlabel("Number of Queens")
plt.ylabel("Time to resolve")
plt.legend(["Min", "Avg", "Max"])
plt.grid(True)
plt.show()

plt.plot(n, yStepsMin)
plt.plot(n, yStepsAvg)
plt.plot(n, yStepsMax)
plt.xlabel("Number of Queens")
plt.ylabel("Number of steps to resolve")
plt.legend(["Min", "Avg", "Max"])
plt.grid(True)
plt.show()

plt.plot(n, yNoSolutions)
plt.xlabel("Number of Queens")
plt.ylabel("Number of failure")
plt.grid(True)
plt.show()

