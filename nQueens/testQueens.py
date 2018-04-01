import nQueens as nq
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# Time test and step test in max 10000 steps with Min-Conflict with Assignment not random

n = [8, 16, 24, 32, 48, 64, 96, 128]
k = 10
steps = 10000

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

        p.setMinConflictsRandomX()

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
plt.ylabel("Time to resolve in seconds")
plt.legend(["Min", "Avg", "Max"])
plt.title("Min-Conflicts with Conflict Initial Assignment")
plt.grid(True)
plt.show()

plt.plot(n, yStepsMin)
plt.plot(n, yStepsAvg)
plt.plot(n, yStepsMax)
plt.xlabel("Number of Queens")
plt.ylabel("Number of steps to resolve")
plt.legend(["Min", "Avg", "Max"])
plt.title("Min-Conflicts with Conflict Initial Assignment")
plt.grid(True)
plt.show()

plt.plot(n, yNoSolutions)
plt.xlabel("Number of Queens")
plt.ylabel("Number of failure")
plt.title("Min-Conflicts with Conflict Initial Assignment")
plt.grid(True)
plt.show()

print yTimeMin
print
print yTimeAvg
print
print yTimeMax

'''

# Min-conflicts with random assignment vs with min conflict initial assignment

n = [8, 16, 24, 32, 64]
k = 10
steps = 10000

yTimeMin = list()
yTimeAvg = list()
yTimeMax = list()

yTimeRMin = list()
yTimeRAvg = list()
yTimeRMax = list()

for i in range(len(n)):
    yTimeTmp = list()
    yTimeRTmp = list()

    for j in range(k):
        p = nq.Problem(n[i])

        p.setMinConflictsRandomX()

        start = timer()
        current = nq.minConflicts(p, steps)
        end = timer()

        yTimeTmp.append(end - start)

        p.setRandomX()

        start = timer()
        current = nq.minConflicts(p, steps)
        end = timer()

        yTimeRTmp.append(end - start)

    yTimeMin.append(min(yTimeTmp))
    yTimeAvg.append(np.average(yTimeTmp))
    yTimeMax.append(max(yTimeTmp))

    yTimeRMin.append(min(yTimeRTmp))
    yTimeRAvg.append(np.average(yTimeRTmp))
    yTimeRMax.append(max(yTimeRTmp))

plt.plot(n, yTimeMin)
plt.plot(n, yTimeAvg)
plt.plot(n, yTimeMax)
plt.xlabel("Number of Queens")
plt.ylabel("Time to resolve in seconds")
plt.legend(["Min", "Avg", "Max"])
plt.title("Min-Conflicts with Conflict Initial Assignment")
plt.grid(True)
plt.show()

plt.plot(n, yTimeRMin)
plt.plot(n, yTimeRAvg)
plt.plot(n, yTimeRMax)
plt.xlabel("Number of Queens")
plt.ylabel("Time to resolve in seconds")
plt.legend(["Min", "Avg", "Max"])
plt.title("Min-Conflicts with Random Initial Assignment")
plt.grid(True)
plt.show()

'''