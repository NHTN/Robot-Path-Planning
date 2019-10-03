import matplotlib.pyplot as plt


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


def getPos(point):
    return ((point[0]-1)*borderLimit[0]+point[1])

visited = []
for i in range(0, (borderLimit[0]+2)*(borderLimit[1]+2)):
    visited.append(0)
pre = []
for i in range(0, borderLimit[0]+1):
    pre += [[(0, 0)] * (borderLimit[1]+1)]

def bfsPath(start, goal):
    for i in range(0, borderLimit[1]):
        canMoveTo[0][i] = 4
        canMoveTo[borderLimit[0]][i] = 4

    for j in range(0, borderLimit[0]):
        canMoveTo[j][0] = 4
        canMoveTo[j][borderLimit[1]] = 4
    canMoveTo[borderLimit[0]][borderLimit[1]] = 4
    
    queue = []
    queue.append([0, start])
    canMoveTo[start[0]][start[1]] = 5

    while queue:
        du, u = queue.pop(0)
        if all(visited):
            break
        visited[getPos(u)] = 1
        
        if (u[0] > 1  and canMoveTo[u[0]-1][u[1]] == 1):
            canMoveTo[u[0]-1][u[1]] = 5
            pre[u[0]-1][u[1]] = u
            queue += [[du+1, [u[0]-1, u[1]]]]

        if (u[0] < borderLimit[0]-1  and canMoveTo[u[0]+1][u[1]] == 1):
            canMoveTo[u[0]+1][u[1]] = 5
            pre[u[0]+1][u[1]] = u
            queue += [[du+1, [u[0]+1, u[1]]]]

        if (u[1] > 1 and canMoveTo[u[0]][u[1]-1] == 1):
            canMoveTo[u[0]][u[1]-1] = 5
            pre[u[0]][u[1]-1] = u
            queue += [[du+1, [u[0], u[1]-1]]]

        if (u[1] < borderLimit[1]-1 and canMoveTo[u[0]][u[1]+1] == 1):
            canMoveTo[u[0]][u[1]+1] = 5
            pre[u[0]][u[1]+1] = u
            queue += [[du+1, [u[0], u[1]+1]]]


polyList = []
for i in range(0, polyCount):
    temp = []
    for j in range(0, int(len(polys[i])/2)):
        temp.append((polys[i][j*2], polys[i][j*2+1]))
    polyList.append(temp)

canMoveTo = []
for i in range(0, borderLimit[0]+1):
    canMoveTo += [[1] * (borderLimit[1]+1)]


def bresehamLine(p0, p1):
    x0, y0 = p0
    x1, y1 = p1

    dx = abs(x1-x0)
    dy = abs(y1-y0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1

    if y0 < y1:
        sy = 1
    else:
        sy = -1
    err = dx-dy
    while True:
        canMoveTo[x0][y0] = 0
        if x0 == x1 and y0 == y1:
            return
        e2 = 2*err
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 < dx:
            err = err + dx
            y0 = y0 + sy

def drawPolygon():
    for i in range(0, polyCount):
        for j in range(0, len(polyList[i])):
            if (j == len(polyList[i])-1):
                bresehamLine(polyList[i][j], polyList[i][0])
            else:
                bresehamLine(polyList[i][j], polyList[i][j+1])


drawPolygon()
bfsPath(start, goal)

temp = pre[goal[0]][goal[1]]
while (temp != start):
    canMoveTo[temp[0]][temp[1]] = 8
    temp = pre[temp[0]][temp[1]]


canMoveTo[start[0]][start[1]] = 2
canMoveTo[goal[0]][goal[1]] = 3
plt.matshow(canMoveTo)
plt.show()

