import matplotlib.pyplot as plt      # Thư viện vẽ đồ thị
from heapq import heappush, heappop  # Thư viện heap - dùng trong thuật toán Dijkstra
import random

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


# Khởi tạo data
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

def canMoveNextStep(nextPosition, nextMove, mat):
    if (nextPosition == (-1, 1) and mat[nextMove[0]][nextMove[1]-1] == 0 and mat[nextMove[0]+1][nextMove[1]] == 0):
        return False
    if (nextPosition == (1, -1) and mat[nextMove[0]-1][nextMove[1]] == 0 and mat[nextMove[0]][nextMove[1]+1] == 0):
        return False
    if (nextPosition == (1, 1) and mat[nextMove[0]][nextMove[1]-1] == 0 and mat[nextMove[0]-1][nextMove[1]] == 0):
        return False
    if (nextPosition == (-1, -1) and mat[nextMove[0]][nextMove[1]+1] == 0 and mat[nextMove[0]+1][nextMove[1]] == 0):
        return False
    return True

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
            if (canMoveTo[nextMove[0]][nextMove[1]] == 1 and dist[nextMove[0]][nextMove[1]] > du + 1.0):
                canMoveTo[nextMove[0]][nextMove[1]] = 5
                pre[nextMove[0]][nextMove[1]] = u
                dist[nextMove[0]][nextMove[1]] = du+1.0
                queue += [[du+1.0, [nextMove[0], nextMove[1]]]]

        for nextPosition in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveNextStep(nextPosition, nextMove, canMoveTo) == False):
                    continue
            if (canMoveTo[nextMove[0]][nextMove[1]] == 1 and dist[nextMove[0]][nextMove[1]] > du + 1.5):
                canMoveTo[nextMove[0]][nextMove[1]] = 5
                pre[nextMove[0]][nextMove[1]] = u
                dist[nextMove[0]][nextMove[1]] = du + 1.5
                queue += [[du+1.5, [nextMove[0], nextMove[1]]]]
            
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
        canMoveTo[u[0]][u[1]] = 5

        for nextPosition in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveTo[nextMove[0]][nextMove[1]] == 1 and dist[nextMove[0]][nextMove[1]] > du + 1.0):
                canMoveTo[nextMove[0]][nextMove[1]] = 5
                pre[nextMove[0]][nextMove[1]] = u
                dist[nextMove[0]][nextMove[1]] = du + 1
                heappush(heap, [(du+1), [nextMove[0], nextMove[1]]])
        
        for nextPosition in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveNextStep(nextPosition, nextMove, canMoveTo)):
                continue
            if (canMoveTo[nextMove[0]][nextMove[1]] == 1 and dist[nextMove[0]][nextMove[1]] > du + 1.5 ):
                canMoveTo[nextMove[0]][nextMove[1]] = 5
                pre[nextMove[0]][nextMove[1]] = u
                dist[nextMove[0]][nextMove[1]] = du + 1.5
                heappush(heap, [(du+1.5), [nextMove[0], nextMove[1]]])

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
#drawPath()
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0.0
        self.h = 0.0
        self.f = 0.0

    def __eq__(self, other):
        return self.position == other.position
# Thuật toán 3: Heuristic - A*
def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0.0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0.0

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
        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if maze[node_position[0]][node_position[1]] != 1:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)


        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1.0
            child.h = (abs(child.position[0] - end_node.position[0])) + abs((child.position[1] - end_node.position[1]))
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)

        childrenCross = []
        for new_position in [(-1, -1), (-1, 1), (1, -1), (1, 1)]: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if maze[node_position[0]][node_position[1]] != 1:
                continue
            if (canMoveNextStep(new_position, node_position, maze) == False):
                continue
            new_node = Node(current_node, node_position)
            childrenCross.append(new_node)

        for child in childrenCross:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1.5
            child.h = (abs(child.position[0] - end_node.position[0]))  + abs((child.position[1] - end_node.position[1]))
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)
        

#path = astar(canMoveTo, (2, 2), (19, 16))
#astar(canMoveTo, (5, 10), (goal[0], goal[1]))


mid = [[2, 2], [3, 4], [19, 16]]

# Đường đi ngắn nhất giữa mọi cặp đỉnh trong tập mid
# Ví dụ: shortest[u][v] là đường đi ngắn nhất giữa mid[u] và mid[v]
shortest = []
for i in range(len(mid)):
    shortest += [[None] * (len(mid))]

# Giải thuật di truyền
# Mỗi cá thể là một lộ trình, có thứ tự và không lặp lại của các đỉnh
# Ví dụ: [4, 2, 3, 1] là một cá thể (đỉnh đầu 0 và cuối len(mid) - 1 là cố định, nên không cần đưa vào)
# Thể hiện đường đi: mid[0] -> mid[4] -> mid[2] -> mid[3] -> mid[1] -> mid[5]
def genetic(mat, mid):

    # Hàm lai 2 cá thể a và b, trả về 2 cá thể mới
    # Chọn một vị trí ngẫu nhiên trong gene, rồi hoán đổi
    def cross(a, b):
        c, d = a, b
        pos = random.randrange(len(a))
        c[pos:], d[pos:] = d[pos:], c[pos:]
        return c, d

    # Hàm đánh giá độ thích nghi của một cá thể a
    # Tính bằng tổng độ dài đoạn đường
    # Hàm có giá trị càng thấp <=> cá thể càng tốt
    # Nếu có 2 đỉnh giống nhau trong cùng một gene, trả về số lớn vô cùng
    # Do mỗi đỉnh chỉ đi qua một lần
    def rate(a):
        visited = []
        for i in range(len(a)):
            visited += [False]
        visited = [False] + visited + [True]
        moreA = [0] + a + [len(a) + 1]
        total = 0
        for i in range(len(moreA) - 1):
            visited[moreA[i]] = True
            total += shortest[moreA[i]][moreA[i + 1]]
        if all(visited):
            return total
        return 999999999999999999999999999

    # BFS với queue đơn giản để tìm đường đi ngắn nhất giữa mọi cặp đỉnh
    # BFS + queue trên ma trận => đường đi hiển nhiên là ngắn nhất
    for u in mid:
        shortest[mid.index(u)][mid.index(u)] = 999999999999999999
        visited = []
        for v in mid:
            if mid.index(v) <= mid.index(u):
                visited += [True]
            else:
                visited += [False]
        distance = []
        for row in range(len(mat) + 1):
            distance += [[None] * (len(mat[0]) + 1)]
        distance[u[0]][u[1]] = 0
        queue = [[0, u]]
        while len(queue) != 0:
            dv, v = queue.pop(0)
            if v in mid and not visited[mid.index(v)]:
                visited[mid.index(v)] = True
                shortest[mid.index(u)][mid.index(v)] = shortest[mid.index(v)][mid.index(u)] = dv
            if all(visited):
                break

            for nextPosition in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nextMove = (v[0]+nextPosition[0], v[1]+nextPosition[1])
                if (mat[nextMove[0]][nextMove[1]] == 1 and distance[nextMove[0]][nextMove[1]] is None):
                    distance[nextMove[0]][nextMove[1]] = dv + 1
                    queue += [[dv + 1, [nextMove[0], nextMove[1]]]]
      
              
            for nextPosition in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                nextMove = (v[0]+nextPosition[0], v[1]+nextPosition[1])
                if mat[nextMove[0]][nextMove[1]] == 1 and distance[nextMove[0]][nextMove[1]] is None:
                    if (canMoveNextStep(nextPosition, nextMove, mat) == False):
                        continue
                    distance[nextMove[0]][nextMove[1]] = dv + 1.5
                    queue += [[dv + 1.5, [nextMove[0], nextMove[1]]]]      


    # Tạo quần thể 600 cá thể
    population = []
    for i in range(600):
        child = [x + 1 for x in range(len(mid) - 2)]
        random.shuffle(child)
        population += [[rate(child), child]]

    # Lai ghép qua 200 đời
    # Mỗi đời bỏ đi 200 cá thể xấu nhất
    # 400 cá thể còn lại cho lai với nhau, tạo ra 200 cá thể mới
    for i in range(200):
        population.sort(key = lambda x: x[0])
        del(population[400:])
        for j in range(0, 399, 2):
            a, b = population[j][1], population[j + 1][1]
            c, d = cross(a, b)
            population += [[rate(c), c], [rate(d), d]]

    # In ra 50 cá thể thích nghi tốt nhất
    population.sort(key = lambda x: x[0])
    for x, y in population[:1]:
        path = [0] + y + [len(mid) - 1]
        for i in range(0, len(path)-1):
            astar(canMoveTo, (mid[i][0], mid[i][1]), (mid[i+1][0], mid[i+1][1]))
        print('Path: {}, distance: {}'.format(path, x))

genetic(canMoveTo, mid)

canMoveTo[start[0]][start[1]] = 2
canMoveTo[goal[0]][goal[1]] = 3

# Biểu diễn đường đi trên đồ thị
plt.matshow(canMoveTo)
plt.show()