import matplotlib.pyplot as plt      # Thư viện vẽ đồ thị
from heapq import heappush, heappop  # Thư viện heap - dùng trong thuật toán Dijkstra


# --------------------------------------------------------------#
# Global variable
borderLimit = [0, 0]    # Toạ độ giới hạn của hình chữ nhật
start = [0, 0]          # Toạ độ điểm bắt đầu
goal = [0, 0]           # Toạ độ điểm đích
polyCount = 0           # Số lượng đa giác 
polys = []              # Danh sách toạ độ các đa giác

polyList = []
canMoveTo = []
pre = []
#---------------------------------------------------------------#

# Đọc dữ liệu từ file input
f = open('input.txt')
borderLimit[0], borderLimit[1] = eval(f.readline())
start[0], start[1], goal[0], goal[1] = eval(f.readline())
polyCount = eval(f.readline())
for line in f:
    polys += [eval(line)]
f.close()


# Kh data 
for i in range(0, polyCount):
    temp = []
    for j in range(0, int(len(polys[i])/2)):
        temp.append((polys[i][j*2], polys[i][j*2+1]))
    polyList.append(temp)

for i in range(0, borderLimit[0]+1):
    canMoveTo += [[1] * (borderLimit[1]+1)]
    pre += [[(0, 0)] * (borderLimit[1]+1)]

    

# Hàm chuyển toạ độ Oxy thành vị trí trên ma trận
def getPos(point):
    return ((point[0]-1)*borderLimit[0]+point[1])

# Thuật toán 1: Bfs duyệt đồ thị theo chiều rộng để tìm đường đi ngắn nhất
def bfsPath(start, goal):
    queue = []
    queue.append([0, start])
    canMoveTo[start[0]][start[1]] = 5
    dist = []
    for i in range(0, borderLimit[0]+1):
        dist += [[float(999999)] * (borderLimit[1]+1)]
    dist[start[0]][start[1]] = 0

    while queue:
        du, u = queue.pop(0)
        
        for nextPosition in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveTo[nextMove[0]][nextMove[1]] != 1 or dist[nextMove[0]][nextMove[1]] <= du + 1.0):
                continue
            canMoveTo[nextMove[0]][nextMove[1]] = 5
            pre[nextMove[0]][nextMove[1]] = u
            dist[nextMove[0]][nextMove[1]] = du+1.0
            queue += [[du+1, [nextMove[0], nextMove[1]]]]
            

# Thuật toán 2: Dijkstra tìm kiếm đường đi ngắn nhất 
def dijkstraPath(start, goal):
    dist = []
    for i in range(0, borderLimit[0]+1):
        dist += [[float(999999)] * (borderLimit[1]+1)]
    dist[start[0]][start[1]] = 0

    heap = []
    heappush(heap, (0, start))

    while (len(heap) != 0):
        du, u = heappop(heap)
        du = -du
        canMoveTo[u[0]][u[1]] = 5

        for nextPosition in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveTo[nextMove[0]][nextMove[1]] != 1 or dist[nextMove[0]][nextMove[1]] <= du + 1.0):
                continue
            canMoveTo[nextMove[0]][nextMove[1]] = 5
            pre[nextMove[0]][nextMove[1]] = u
            dist[nextMove[0]][nextMove[1]] = du + 1
            heappush(heap, [-(du+1), [nextMove[0], nextMove[1]]])

# Thuật toán bresehamLine vẽ đường thẳng từ 2 điểm p0 - p1
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

# Tô màu các polygon 
def drawPolygon():
    for i in range(0, polyCount):
        for j in range(0, len(polyList[i])):
            if (j == len(polyList[i])-1):
                bresehamLine(polyList[i][j], polyList[i][0])
            else:
                bresehamLine(polyList[i][j], polyList[i][j+1])

# Tô màu khung hình chữ nhật
def drawBorder():
    for i in range(0, borderLimit[1]):
        canMoveTo[0][i] = 4
        canMoveTo[borderLimit[0]][i] = 4

    for j in range(0, borderLimit[0]):
        canMoveTo[j][0] = 4
        canMoveTo[j][borderLimit[1]] = 4
    canMoveTo[borderLimit[0]][borderLimit[1]] = 4

# Tô màu đường đi 
def drawPath():
    temp = pre[goal[0]][goal[1]]
    while (temp != start):
        canMoveTo[temp[0]][temp[1]] = 8
        temp = pre[temp[0]][temp[1]]

# ----------------------------------   Main program ----------------------------------------- # 
drawPolygon()
drawBorder()

# Tìm kiếm mù
#bfsPath(start, goal)
# Tham lam
#dijkstraPath(start, goal)

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
# Thuật toán 3: Heuristic - A*
def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                canMoveTo[current.position[0]][current.position[1]] = 5
                current = current.parent
            return path[::-1] 

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if maze[node_position[0]][node_position[1]] != 1:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)

#path = astar(canMoveTo, (2, 2), (19, 16))
astar(canMoveTo, (start[0], start[1]), (goal[0], goal[1]))

canMoveTo[start[0]][start[1]] = 2
canMoveTo[goal[0]][goal[1]] = 3

# Biểu diễn đường đi trên đồ thị
plt.matshow(canMoveTo)
plt.show()