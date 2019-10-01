
borderLimit = [0, 0]
start = [0, 0]
goal = [0, 0]
polyCount = 0
polys = []

f = open('input.txt')
borderLimit[0], borderLimit[1] = eval(f.readline())
start[0], start[1], goal[0], goal[1] = eval(f.readline())
polyCount = eval(f.readline())
for line in f:
    polys += [eval(line)]
f.close()

print(polys)


mark = []
for i in range(100):
    mark.append(0)

# Check if a point is inside a polygon
def onSegment(a, b, c): 
    return (b[0] <= max(a[0], c[0]) and b[0] >= min(a[0], c[0]) and b[1] <= max(a[1], c[1]) and b[1] >= min(a[1], c[1]))

def orientation(a, b, c):
    val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    if (val == 0): return 0
    if (val > 0): return 1
    return 2

def doIntersect(p1, q1, p2, q2):
    case1 = orientation(p1, q1, p2)
    case2 = orientation(p1, q1, q2)
    case3 = orientation(p2, q2, p1)
    case4 = orientation(p2, q2, q1)

    if (case1 != case2 and case3 != case4): return True

    if (case1 == 0 and onSegment(p1, p2, q1)): 
        return True
    if (case2 == 0 and onSegment(p1, q2, q1)): 
        return True
    if (case3 == 0 and onSegment(p2, p1, q2)): 
        return True
    if (case4 == 0 and onSegment(p2, q1, q2)): 
        return True

    return False

def isInside(polygon, nEdge, checkPoint):
    if (nEdge < 3 ): 
        return False
    count = 0
    i = 0

    extreme = (10000, checkPoint[1])
    while True:
        next = (i+1)%nEdge
        if (doIntersect(polygon[i+1], polygon[next+1], checkPoint, extreme)):
            if (orientation(polygon[i+1], checkPoint, polygon[next+1]) == 0):
                return onSegment(polygon[i+1], checkPoint, polygon[next+1])
            count += 1
        i = next
        if (i == 0): break

   # print((i+1)%nEdge)
    return count&1 #count%2 == 1

def getDistance(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])


def getPos(point):
    return ((point[0]-1)*borderLimit[0]+point[1])

def dfsPath(start, goal, path):
    path.append(start)
    if (getPos(start) == getPos(goal)): 
        return True

    nextStep = []
    del nextStep[:]
    if (start[0] > 1):
        nextStep.append(((start[0]-1, start[1]), 1))
    if (start[0] < borderLimit[0]-1):
        nextStep.append(((start[0]+1, start[1]), 1)) 
    if (start[1] > 1):
        nextStep.append(((start[0], start[1]-1), 1))
    if (start[1] < borderLimit[1]-1):
        nextStep.append(((start[0], start[1]+1), 1))

    for next in range(0, len(nextStep)):
        v = getPos(nextStep[next][0])
        if ((mark[v] == 0)):
            mark[v] = 1
            dfsPath(nextStep[next][0], goal, path)
            
path = []
mark[getPos(start)] = 1
dfsPath(start, goal, path)
print(path)

canMoveTo = []
for i in range(1, (borderLimit[0]+1)*(borderLimit[1]+1)):
    canMoveTo.append(True)

for xCoordinate in range(1, borderLimit[0]+1):
    for yCoordinate in range(1, borderLimit[1]+1):
        tempPoint = (xCoordinate, yCoordinate)
        for i in range(0, polyCount):
            print(polys[i]), 
            print(xCoordinate), 
            print(yCoordinate)
            '''
            if (isInside(polys[i], polys[i][0], tempPoint)):
                print(getPos(tempPoint))
                canMoveTo[getPos(tempPoint)] = False'''
        
print(canMoveTo)
print(isInside(polys[0], polys[0][0], (1, 1)))