import matplotlib.pyplot as plt      # Thư viện vẽ đồ thị
from heapq import heappush, heappop  # Thư viện heap - dùng trong thuật toán Dijkstra


# --------------------------------------------------------------#
# Global variable
borderLimit = [0, 0]    # Toạ độ giới hạn của hình chữ nhật
start = [0, 0]          # Toạ độ điểm bắt đầu
goal = [0, 0]           # Toạ độ điểm đích
polyCount = 0           # Số lượng đa giác 
polys = []              # Danh sách toạ độ các đa giác
#---------------------------------------------------------------#



# Đọc dữ liệu từ file input
f = open('input.txt')
borderLimit[0], borderLimit[1] = eval(f.readline())
start[0], start[1], goal[0], goal[1] = eval(f.readline())
polyCount = eval(f.readline())
for line in f:
    polys += [eval(line)]
f.close()

# Hàm chuyển toạ độ Oxy thành vị trí trên ma trận
def getPos(point):
    return ((point[0]-1)*borderLimit[0]+point[1])

# Mảng lưu trữ truy vết đường đi
pre = []
for i in range(0, borderLimit[0]+1):
    pre += [[(0, 0)] * (borderLimit[1]+1)]

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
        
        if (canMoveTo[u[0]-1][u[1]] == 1 and dist[u[0]-1][u[1]] > du + 1.0):
            canMoveTo[u[0]-1][u[1]] = 5
            pre[u[0]-1][u[1]] = u
            dist[u[0]-1][u[1]] = du + 1.0
            queue += [[du+1, [u[0]-1, u[1]]]]

        if (canMoveTo[u[0]+1][u[1]] == 1  and dist[u[0]+1][u[1]] > du + 1.0):
            canMoveTo[u[0]+1][u[1]] = 5
            pre[u[0]+1][u[1]] = u
            dist[u[0]+1][u[1]] = du + 1.0
            queue += [[du+1, [u[0]+1, u[1]]]]

        if (canMoveTo[u[0]][u[1]-1] == 1 and dist[u[0]][u[1]-1] > du + 1.0):
            canMoveTo[u[0]][u[1]-1] = 5
            pre[u[0]][u[1]-1] = u
            dist[u[0]][u[1]-1] = du + 1.0
            queue += [[du+1, [u[0], u[1]-1]]]

        if (canMoveTo[u[0]][u[1]+1] == 1 and dist[u[0]][u[1]+1] > du + 1.0):
            canMoveTo[u[0]][u[1]+1] = 5
            pre[u[0]][u[1]+1] = u
            dist[u[0]][u[1]+1] = du + 1.0
            queue += [[du+1, [u[0], u[1]+1]]]

    print(dist[goal[0]][goal[1]])

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

        # Đi qua phải
        if (canMoveTo[u[0]-1][u[1]] == 1 and dist[u[0]-1][u[1]] > du + 1.0):
            canMoveTo[u[0]-1][u[1]] = 5
            pre[u[0]-1][u[1]] = u
            dist[u[0]-1][u[1]] = du + 1.0
            heappush(heap, [-(du+1), [u[0]-1, u[1]]])
        # Đi qua trái
        if (canMoveTo[u[0]+1][u[1]] == 1 and dist[u[0]+1][u[1]] > du + 1.0):
            canMoveTo[u[0]+1][u[1]] = 5
            pre[u[0]+1][u[1]] = u
            dist[u[0]-1][u[1]] = du + 1.0
            heappush(heap, [-(du+1), [u[0]+1, u[1]]])
        # Đi lên trên
        if (canMoveTo[u[0]][u[1]-1] == 1 and dist[u[0]][u[1]-1] > du + 1.0):
            canMoveTo[u[0]][u[1]-1] = 5
            pre[u[0]][u[1]-1] = u
            dist[u[0]][u[1]-1] = du + 1.0
            heappush(heap, [-(du+1), [u[0], u[1]-1]])
        # Đi xuống dưới
        if (canMoveTo[u[0]][u[1]+1] == 1 and dist[u[0]][u[1]+1] > du + 1.0):
            canMoveTo[u[0]][u[1]+1] = 5
            pre[u[0]][u[1]+1] = u
            dist[u[0]][u[1]+1] = du + 1.0
            heappush(heap, [-(du+1), [u[0], u[1]+1]])
'''
        # Đi chéo đông - bắc
        if (canMoveTo[u[0]+1][u[1]+1] == 1 and dist[u[0]+1][u[1]+1] > du + 1.5):
            canMoveTo[u[0]+1][u[1]+1] = 5
            pre[u[0]+1][u[1]+1] = u
            dist[u[0]+1][u[1]+1] = du + 1.5
            heappush(heap, [-(du+1), [u[0]+1, u[1]+1]])
        #Đi chéo tây - bắc
        if (canMoveTo[u[0]-1][u[1]+1] == 1 and dist[u[0]-1][u[1]+1] > du + 1.5):
            canMoveTo[u[0]-1][u[1]+1] = 5
            pre[u[0]-1][u[1]+1] = u
            dist[u[0]-1][u[1]+1] = du + 1.5
            heappush(heap, [-(du+1), [u[0]-1, u[1]+1]])
        #Đi chéo đông - nam
        if (canMoveTo[u[0]+1][u[1]-1] == 1 and dist[u[0]+1][u[1]-1] > du + 1.5):
            canMoveTo[u[0]+1][u[1]-1] = 5
            pre[u[0]+1][u[1]-1] = u
            dist[u[0]+1][u[1]-1] = du + 1.5
            heappush(heap, [-(du+1), [u[0]+1, u[1]-1]])
        # Đi chéo tây - nam
        if (canMoveTo[u[0]-1][u[1]+1] == 1 and dist[u[0]][u[1]+1] > du + 1.5):
            canMoveTo[u[0]-1][u[1]+1] = 5
            pre[u[0]-1][u[1]+1] = u
            dist[u[0]-1][u[1]+1] = du + 1.5
            heappush(heap, [-(du+1), [u[0]-1, u[1]+1]])
'''


polyList = []
for i in range(0, polyCount):
    temp = []
    for j in range(0, int(len(polys[i])/2)):
        temp.append((polys[i][j*2], polys[i][j*2+1]))
    polyList.append(temp)


canMoveTo = []
for i in range(0, borderLimit[0]+1):
    canMoveTo += [[1] * (borderLimit[1]+1)]

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
dijkstraPath(start, goal)


drawPath()

canMoveTo[start[0]][start[1]] = 2
canMoveTo[goal[0]][goal[1]] = 3

# Biểu diễn đường đi trên đồ thị
plt.matshow(canMoveTo)
plt.show()

