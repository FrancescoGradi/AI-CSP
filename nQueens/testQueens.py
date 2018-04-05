import nQueens as nq
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# Time test and step test in max 10000 steps with Min-Conflict with Assignment not random

n = [8, 16, 20, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128]
k = 10
steps = 10000

yTimeMin = list()
yTimeAvg = list()
yTimeMax = list()

yStepsMin = list()
yStepsAvg = list()
yStepsMax = list()

yNoSolutions = list()

startTest = timer()

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

    print "Finished " + str(n[i]) + " queens"

    yTimeMin.append(min(yTimeTmp))
    yTimeAvg.append(np.average(yTimeTmp))
    yTimeMax.append(max(yTimeTmp))

    yStepsMin.append(min(yStepsTmp))
    yStepsAvg.append(np.average(yStepsTmp))
    yStepsMax.append(max(yStepsTmp))

endTest = timer()

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

print "Time test: " + str(endTest - startTest)

print yTimeMin
print
print yTimeAvg
print
print yTimeMax
print
print yStepsMin
print
print yStepsAvg
print
print yStepsMax
print
print yNoSolutions

'''

# Min-conflicts with random assignment vs with min conflict initial assignment

n = [8, 16, 24, 32, 64]
k = 10
steps = 10000

yTimeAvg = list()

yTimeRAvg = list()

startTest = timer()

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

    yTimeAvg.append(np.average(yTimeTmp))

    yTimeRAvg.append(np.average(yTimeRTmp))

endTest = timer()

print "Time test: " + str(endTest - startTest)

plt.plot(n, yTimeAvg)
plt.plot(n, yTimeRAvg)
plt.xlabel("Number of Queens")
plt.ylabel("Time to resolve in seconds")
plt.legend(["Conflict Initial Assignment", "Random Initial Assignment"])
plt.title("Min-Conflicts with Conflict Initial Assignment VS Random Initial Assignment")
plt.grid(True)
plt.show()

'''