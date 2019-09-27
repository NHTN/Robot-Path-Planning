import math

def getPosition(x, y):
    return x + y*(border.y+1)

class Point:
    def __init__(self, xCoordinate, yCoordinate):
        self.x = xCoordinate
        self.y = yCoordinate
        self.position = getPosition(xCoordinate, yCoordinate)

class Polygon:
    def __init__(self, nEdge, lPoint):
        self.numOfEdge = nEdge
        self.pointList = lPoint


# Global variable
border = Point          # Limited of rectangle

sourcePoint = Point     # Source coordinate 
destPoint = Point       # Dest coordinate

numPolygons = 0         # Number of polygons in rectangle 
polygonList = []        # List of polygons coordinate

canMoveTo = []          # 


# Read data from file and parse to variable
def initData():
    with open("input.txt", "r") as inputFile:
        inputArr = []
        for line in inputFile:
            inputArr.append([int(x) for x in line.split()])

    border.x = inputArr[0][0] 
    border.y = inputArr[0][1]

    sourcePoint.x = inputArr[1][0]
    sourcePoint.y = inputArr[1][1]
    destPoint.x = inputArr[1][2]
    destPoint.y = inputArr[1][3]

    numPolygons = [int(inputArr[2][0])]

    for polyNum in numPolygons:
        pointTemp = []
        for edgeNum in range(0, inputArr[polyNum+2][0]):
            pointTemp.append(Point(inputArr[polyNum+2][edgeNum*2+1], inputArr[polyNum+2][edgeNum*2+2]))  
        
        polygonList.append(Polygon(inputArr[polyNum+2][0], pointTemp))

# Check if a point is inside a polygon
def onSegment(a, b, c): 
    return (b.x <= max(a.x, c.x) and b.x >= min(a.x, c.x) and b.y <= max(a.y, c.y) and b.y >= min(a.y, c.y))

def orientation(a, b, c):
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
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
    if (nEdge < 3 ): return False
    count = 0
    i = 0

    extreme = Point(10000, checkPoint.y)
    while True:
        next = (i+1)%nEdge
        if (doIntersect(polygon[i], polygon[next], checkPoint, extreme)):
            if (orientation(polygon[i], checkPoint, polygon[next]) == 0):
                return onSegment(polygon[i], checkPoint, polygon[next])
            count += 1
        i = next
        if (i == 0): break

   # print((i+1)%nEdge)
    return count&1 #count%2 == 1

def getDistance(p, q):
    return abs(p.x-q.x) + abs(p.y-q.y)

# Main Program
initData()

graphDistance = [[0]*(border.x+1)*(border.y+1)]*(border.y+1)*(bo)   


for i in range(1, border.x): 
    for j in range(1, border.y):
        for u in range(1, border.x):
            for v in range(1, border.y): 
                pointA = Point(i, j)
                pointB = Point(u, v)
            
                for poly in range(0, len(polygonList)):
                    for edge in range(0, polygonList[poly].numOfEdge-1):
                        pointC = Point(0, 0)
                        pointD = Point(0, 0)
                        pointC = polygonList[poly].pointList[edge]
                        if (edge == (polygonList[poly].numOfEdge)): 
                            pointD = polygonList[poly].pointList[0]
                        else: 
                            pointD = polygonList[poly].pointList[edge+1]
                        if (doIntersect(pointA, pointB, pointC, pointD)):
                            graphDistance[getPosition(i, j)][getPosition(u, v)] = -1
                        else: 1
                         #   graphDistance[getPosition(i, j)][getPosition(u, v)] = getDistance(pointA, pointB)


print(graphDistance[1][2])
'''
for i in range(1, (border.x+1)*(border.y+1)):
    canMoveTo.append(True)

for xCoordinate in range(1, border.x+1):
    for yCoordinate in range(1, border.y+1):
        tempPoint = Point(xCoordinate, yCoordinate)
        for poly in range(1, len(polygonList)):
            if (isInside(polygonList[poly], polygonList[poly].numOfEdge, tempPoint)):
                canMoveTo[tempPoint.position] = False
        

for i in (1, border.x):
    for j in (1, border.y):
        print(canMoveTo[getPosition(i, j)])
'''
