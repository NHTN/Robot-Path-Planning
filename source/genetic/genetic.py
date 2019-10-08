import random

# Giả định đã vẽ xong ma trận địa hình
# Chỉ có thể đi trên ô có kí tự '.', tất cả kí tự khác đều không đi được
# Tùy biến kí tự '.' theo ý muốn trong phần BFS của hàm genetic
mat = []
f = open('input.txt', 'r')
for line in f:
    line = line.rstrip('\n')
    row = [x for x in line]
    mat += [row]
f.close()

# Giả định input
# Mid là tập các điểm phải đi qua, mid[0] là start, mid[-1] là goal
# Chỉ có điểm đầu và điểm cuối là giữ nguyên
# Các điểm ở giữa phải sắp xếp để được đường đi ngắn nhất
mid = [[2, 2], [3, 3], [19, 16]]

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

            if mat[v[0] - 1][v[1]] == '.' and distance[v[0] - 1][v[1]] is None:
                distance[v[0] - 1][v[1]] = dv + 1
                queue += [[dv + 1, [v[0] - 1, v[1]]]]

            if mat[v[0] + 1][v[1]] == '.' and distance[v[0] + 1][v[1]] is None:
                distance[v[0] + 1][v[1]] = dv + 1
                queue += [[dv + 1, [v[0] + 1, v[1]]]]

            if mat[v[0]][v[1] - 1] == '.' and distance[v[0]][v[1] - 1] is None:
                distance[v[0]][v[1] - 1] = dv + 1
                queue += [[dv + 1, [v[0], v[1] - 1]]]

            if mat[v[0]][v[1] + 1] == '.' and distance[v[0]][v[1] + 1] is None:
                distance[v[0]][v[1] + 1] = dv + 1
                queue += [[dv + 1, [v[0], v[1] + 1]]]

            if mat[v[0] - 1][v[1] - 1] == '.' and distance[v[0] - 1][v[1] - 1] is None and (mat[v[0] - 1][v[1]] == '.' or mat[v[0]][v[1] - 1] == '.'):
                distance[v[0] - 1][v[1] - 1] = dv + 1.5
                queue += [[dv + 1.5, [v[0] - 1, v[1] - 1]]]

            if mat[v[0] - 1][v[1] + 1] == '.' and distance[v[0] - 1][v[1] + 1] is None and (mat[v[0] - 1][v[1]] == '.' or mat[v[0]][v[1] + 1] == '.'):
                distance[v[0] - 1][v[1] + 1] = dv + 1.5
                queue += [[dv + 1.5, [v[0] - 1, v[1] + 1]]]

            if mat[v[0] + 1][v[1] + 1] == '.' and distance[v[0] + 1][v[1] + 1] is None and (mat[v[0] + 1][v[1]] == '.' or mat[v[0]][v[1] + 1] == '.'):
                distance[v[0] + 1][v[1] + 1] = dv + 1.5
                queue += [[dv + 1.5, [v[0] + 1, v[1] + 1]]]

            if mat[v[0] + 1][v[1] - 1] == '.' and distance[v[0] + 1][v[1] - 1] is None and (mat[v[0] + 1][v[1]] == '.' or mat[v[0]][v[1] - 1] == '.'):
                distance[v[0] + 1][v[1] - 1] = dv + 1.5
                queue += [[dv + 1.5, [v[0] + 1, v[1] - 1]]]
    
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
    for x, y in population[:50]:
        path = [0] + y + [len(mid) - 1]
        print('Path: {}, distance: {}'.format(path, x))

genetic(mat, mid)