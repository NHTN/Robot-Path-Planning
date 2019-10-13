import matplotlib.pyplot as plt      # Thư viện vẽ đồ thị
from heapq import heappush, heappop  # Thư viện heap - dùng trong thuật toán Dijkstra
import random

# --------------------------------------------------------------- Global variable ---------------------------------------------------------#

borderLimit = [0, 0]    # Toạ độ giới hạn của hình chữ nhật
start = [0, 0]          # Toạ độ điểm bắt đầu
goal = [0, 0]           # Toạ độ điểm đích
polyCount = 0           # Số lượng đa giác 
polys = []              # Danh sách toạ độ các đa giác

polyList = [] 
canMoveTo = []
trace = []
#-----------------------------------------------------------------------------------------------------------------------------------------#

# Đọc dữ liệu từ file input
f = open('input.txt')
borderLimit[0], borderLimit[1] = eval(f.readline())
start[0], start[1], goal[0], goal[1] = eval(f.readline())
polyCount = eval(f.readline())
for line in f:
    polys += [eval(line)]
f.close()

# Khởi tạo data
def initData(polyCount, polys, polyList, borderLimit, canMoveTo, trace):
    for i in range(0, polyCount):
        temp = []
        for j in range(0, int(len(polys[i])/2)):
            temp.append((polys[i][j*2], polys[i][j*2+1]))
        polyList.append(temp)
    for i in range(0, borderLimit[0]+1):
        canMoveTo += [[1] * (borderLimit[1]+1)]
    for i in range(0, len(canMoveTo)+1):
        trace += [[(0, 0)] * (len(canMoveTo[0])+1)]

# Hàm chuyển toạ độ Oxy thành vị trí trên ma trận
def getPos(point):
    return ((point[0]-1)*borderLimit[0]+point[1])

# Hàm kiểm tra điều kiện cho phép đi chéo ?
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


# -----------------------------------------------------------------------------
# Thuật toán 1: Bfs duyệt đồ thị theo chiều rộng để tìm đường đi ngắn nhất
def BFS(mat, start, goal, trace):
    queue = []
    queue.append([0, start])

    distance = []

    for row in range(0, len(mat)+1):
        distance += [[0.0] * (len(mat[0])+1)]

    distance[start[0]][start[1]] = 0

    while len(queue) > 0:
        du, u = queue.pop(0)
        for nextPosition in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveNextStep(nextPosition, nextMove, mat) == False):
                continue
            if (mat[nextMove[0]][nextMove[1]] == 1 and distance[nextMove[0]][nextMove[1]] == 0.0):
                weight = 1.0
                if (nextPosition in [(-1, -1), (-1, 1), (1, -1), (1, 1)]):
                    weight = 1.5
                trace[nextMove[0]][nextMove[1]] = u
                distance[nextMove[0]][nextMove[1]] = du + weight
                queue += [[du + weight, [nextMove[0], nextMove[1]]]]
    
    return distance[goal[0]][goal[1]]

# Thuật toán 2: USC
def UCS(mat, start, goal, trace):
    distance = []
    for row in range(0, len(mat)+1):
        distance += [[0.0] * (len(mat[0])+1)]
    distance[start[0]][start[1]] = 0

    heap = []
    heappush(heap, (0, start))

    while (len(heap) > 0):
        du, u = heappop(heap)

        for nextPosition in [(1, 0), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (mat[nextMove[0]][nextMove[1]] == 1 and distance[nextMove[0]][nextMove[1]] == 0.0):
                weight = 1.0
                if (nextPosition in [(-1, -1), (-1, 1), (1, -1), (1, 1)]):
                    weight = 1.5
                trace[nextMove[0]][nextMove[1]] = u
                distance[nextMove[0]][nextMove[1]] = du + weight
                heappush(heap, [(du + weight), [nextMove[0], nextMove[1]]])
    print(distance[goal[0]][goal[1]])
    return distance[goal[0]][goal[1]]

# Hàm Heuristic (khoảng cách Euclid)
def euclid(u, v):
    return ((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2) ** (1/2)

# Thuật toán 3: A star
def AStar(mat, start, goal, trace):
    # Khởi tạo distance[i][j] = None với mọi i, j (nghĩa là mọi ô (i, j) đều chưa đi tới)
    distance = []
    for row in range(len(mat) + 1):
        distance += [[0.0] * (len(mat[0]) + 1)]
    
    # distance của start = 0
    distance[start[0]][start[1]] = 0

    # Cho start vào queue
    heap = []
    heappush(heap, [0 + euclid(start, goal), start])

    # Lặp tới khi queue rỗng
    while (len(heap) > 0):
        # Lấy một đỉnh từ queue
        du, u = heappop(heap)
        du = distance[u[0]][u[1]]

        # Nếu đây là đỉnh kết thúc, thoát
        if (u[0] == goal[0] and u[1] == goal[1]):
            break
        # Duyệt các đỉnh kề u
        # Nếu có thể đi được và chưa đi vào (distance is None) 
        # Thì đưa vào queue, đánh dấu đã đi vào
        for nextPosition in [(1, 0), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nextMove = (u[0]+nextPosition[0], u[1]+nextPosition[1])
            if (canMoveTo[nextMove[0]][nextMove[1]] == 1 and distance[nextMove[0]][nextMove[1]] == 0.0):
                weight = 1.0
                if (nextPosition in [(-1, -1), (-1, 1), (1, -1), (1, 1)]):
                    weight = 1.5
                trace[nextMove[0]][nextMove[1]] = u                         
                distance[nextMove[0]][nextMove[1]] = du + weight
                heappush(heap,[(du + weight + euclid(nextMove, goal)), [nextMove[0], nextMove[1]]])

    return distance[goal[0]][goal[1]]

# ------------------------------------------------------------------------------
mid = [[2, 2], [6, 10], [19, 16]]

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
            total =  total + shortest[moreA[i]][moreA[i + 1]]
        if all(visited):
            return total
        return 99999999999

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
            BFS(mat, mid[i], mid[i+1], trace)
            drawPath(mat, trace, mid[i], mid[i+1])
        print('Path: {}, distance: {}'.format(path, x))

# ---------------------------------------------------------------- Mô phỏng đồ thị ------1----------------------------------------------#
# Thuật toán BresenhamLine vẽ đường thẳng từ 2 điểm p0 - p1
def bresenhamLine(p0, p1):
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
def drawPolygon(polyCount, polyList):
    for i in range(0, polyCount):
        for j in range(0, len(polyList[i])):
            if (j == len(polyList[i])-1):
                bresenhamLine(polyList[i][j], polyList[i][0])
            else:
                bresenhamLine(polyList[i][j], polyList[i][j+1])

# Tô màu khung hình chữ nhật
def drawBorder(canMoveTo):
    for row in range(0, borderLimit[1]+1):
        canMoveTo[0][row] = 4
        canMoveTo[borderLimit[0]][row] = 4

    for column in range(0, borderLimit[0]):
        canMoveTo[column][0] = 4
        canMoveTo[column][borderLimit[1]] = 4

# Tô màu đường đi 
def drawPath(canMoveTo, trace, start, goal):
    canMoveTo[start[0]][start[1]] = 2
    canMoveTo[goal[0]][goal[1]] = 3
    temp = trace[goal[0]][goal[1]]
    if (temp == (0, 0)):
        print("No Path")
        return
    while (temp != start):
        canMoveTo[temp[0]][temp[1]] = 8
        temp = trace[temp[0]][temp[1]]
        if (temp == (0, 0)):
            return

# ---------------------------------------------------------------- Mô phỏng đồ thị -----------------------------------------------------#

# ----------------------------------------------------------------  Main program -------------------------------------------------------# 

initData(polyCount, polys, polyList, borderLimit, canMoveTo, trace)
drawBorder(canMoveTo)
drawPolygon(polyCount, polyList)
choice = int(input("Enter your algorithm: "))

while (choice > 0 and choice < 5):
    if (choice == 1):
        print(BFS(canMoveTo, start, goal, trace))
        drawPath(canMoveTo, trace, start, goal)
    elif (choice == 2):
        print(UCS(canMoveTo, start, goal, trace))
        drawPath(canMoveTo, trace, start, goal)
    elif (choice == 3):
        print(AStar(canMoveTo, start, goal, trace))
        drawPath(canMoveTo, trace, start, goal)
    elif (choice == 4):
        genetic(canMoveTo, mid) 

     # Biểu diễn đường đi trên đồ thị
    plt.matshow(canMoveTo)
    plt.show()
    choice = int(input("Enter your algorithm: "))

    for i in range(0, borderLimit[0]):
        for j in range(0, borderLimit[1]): 
            if (canMoveTo[i][j] == 8):
                canMoveTo[i][j] = 1

    


# ----------------------------------------------------------------  Main program -------------------------------------------------------# 