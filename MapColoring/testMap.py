import mapColoring as mp
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

n = [128, 256, 512, 1024, 2048, 4096]
nColors = [5, 5, 5, 5, 5, 6, 6]
k = 10
steps = 100000

# Time test and step test in max 100000 steps

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
        map = mp.getRandomMap(n[i], nColors[i])

        start = timer()

        current = mp.minConflicts(map, steps)

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
plt.xlabel("Number of Regions")
plt.ylabel("Time to resolve")
plt.legend(["Min", "Avg", "Max"])
plt.title("Map Coloring resolution time")
plt.grid(True)
plt.show()

plt.plot(n, yStepsMin)
plt.plot(n, yStepsAvg)
plt.plot(n, yStepsMax)
plt.xlabel("Number of Regions")
plt.ylabel("Number of steps to resolve")
plt.legend(["Min", "Avg", "Max"])
plt.grid(True)
plt.show()

plt.plot(n, yNoSolutions)
plt.xlabel("Number of Regions")
plt.ylabel("Number of failure")
plt.grid(True)
plt.show()