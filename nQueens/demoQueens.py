import nQueens as nq
from timeit import default_timer as timer

n = 16
p = nq.Problem(n)
p.setMinConflictsRandomX()
#p.drawQueens()

print "Initial random assignment: "
print
print p.x

print

print "Running MinConflicts heuristic: "

print

# Min Conflicts

steps = 100000

start = timer()

current = nq.minConflicts(p, steps)

end = timer()

if current is 0:
    print "Solution not found in " + str(steps) + " steps and " + str(end - start) + " seconds"
else:
    print "I found a solution in " + str(current[1]) + " steps " + str(end - start) + " seconds"
    print
    print p.x
    print
    print p.getMatrix()

    p.drawQueens()

'''

# Min Conflicts using Random Restart


steps = 10000
restarts = 15

start = timer()

current = nq.minConflictsRandomRestart(p, steps, restarts)

end = timer()

if current is 0:
    print "Solution not found in " + str(steps) + " steps, " + str(end - start) + " seconds and " + str(restarts) + " random restarts"
else:
    print "I found a solution in " + str(current[1]) + " steps, " + str(end - start) + " seconds and " + str(current[2]) + " random restarts"
    print
    print p.getMatrix()

    #p.drawQueens()
    
'''