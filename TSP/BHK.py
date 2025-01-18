# Bellman-Held-Karp algorithm
import matplotlib.pyplot as plt
import numpy as np

coord = [0.6683,0.2536,0.6195,0.2634,0.4,0.4439,0.2439,0.1463,0.1707,0.2293,
         0.2293,0.761,0.5171,0.9414,0.8732,0.6536,0.6878,0.5219,0.8488,0.3609]
coord = np.array(coord).reshape(10,2) # 点的坐标

# 描点编号
plt.scatter(coord[:,0],coord[:,1], color='w', edgecolors='b')
for i in range(10):
    plt.text(coord[i,0]+0.01, coord[i,1]+0.01, i)
    
# 点的个数
n = coord.shape[0]

# 距离矩阵
d = np.zeros((n,n))
for i in range(n):
    for j in range(i+1,n):
        x_i = coord[i,0]
        y_i = coord[i,1]
        x_j = coord[j,0]
        y_j = coord[j,1]
        d[i,j] = d[j,i] = np.linalg.norm(coord[i] - coord[j])

# Bellman-Held-Karp算法实现并记录路径
def tsp_bhk_with_trace_any_start(dist_matrix):
    n = len(dist_matrix)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]  # 记录路径的前驱节点
    
    # 初始化状态：dp[1<<i][i] = 0，表示从点i出发，其他点未访问
    for i in range(n):
        dp[1 << i][i] = 0
    
    # 填充 dp 表格
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):  # 如果 i 在 mask 集合中
                for j in range(n):
                    if not mask & (1 << j):  # 如果 j 不在 mask 集合中
                        new_mask = mask | (1 << j)
                        new_dist = dp[mask][i] + dist_matrix[i][j]
                        if new_dist < dp[new_mask][j]:
                            dp[new_mask][j] = new_dist
                            parent[new_mask][j] = i  # 记录前驱节点

    # 计算从任意节点出发并回到起点的最短路径
    final_mask = (1 << n) - 1  # 表示所有节点都被访问的状态
    result = float('inf')
    best_start = -1
    last_node = -1

    for i in range(n):
        for j in range(n):
            new_dist = dp[final_mask][i] + dist_matrix[i][j]  # 回到起点 j 的距离
            if new_dist < result:
                result = new_dist
                last_node = i
                best_start = j

    # 回溯路径
    min_path = []
    mask = final_mask
    node = last_node
    while node != -1:
        min_path.append(node)
        next_node = parent[mask][node]
        mask = mask ^ (1 << node)  # 从mask中移除当前节点
        node = next_node

    min_path.append(best_start)  # 闭合路径，回到最佳起点
    min_path.reverse()  # 路径需要反转，因为我们是从终点回溯到起点的

    return result, min_path

# 计算最短路径长度和路径
shortest_path_length, shortest_path = tsp_bhk_with_trace_any_start(d)
print(f"最短路径长度为: {shortest_path_length}")
print(f"最短路径为: {shortest_path}")

# 画出点和最短路径的连线
plt.scatter(coord[:, 0], coord[:, 1], color='w', edgecolors='b')
for i in range(10):
    plt.text(coord[i, 0] + 0.01, coord[i, 1] + 0.01, str(i), fontsize=12)

for i in range(len(shortest_path) - 1):
    xi = coord[shortest_path[i], 0]
    yi = coord[shortest_path[i], 1]
    xj = coord[shortest_path[i + 1], 0]
    yj = coord[shortest_path[i + 1], 1]
    plt.plot([xi, xj], [yi, yj], color='r')

plt.plot([coord[shortest_path[-1], 0], coord[shortest_path[0], 0]],
         [coord[shortest_path[-1], 1], coord[shortest_path[0], 1]], color='r')  # 闭合路径

plt.show()