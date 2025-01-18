# Ant Colony Optimization(ACO)
import matplotlib.pyplot as plt
import numpy as np

class AntColony:
    def __init__(self, dist_matrix, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        self.dist_matrix = dist_matrix
        self.pheromone = np.ones(self.dist_matrix.shape) / len(dist_matrix)
        self.all_inds = range(len(dist_matrix))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self, start_node):
        all_time_shortest_path = None
        shortest_path_length = np.inf

        for i in range(self.n_iterations):
            all_paths = self.construct_colony_paths(start_node)
            self.spread_pheromone(all_paths, self.n_best)
            iteration_shortest_path = min(all_paths, key=lambda x: x[1])
            if iteration_shortest_path[1] < shortest_path_length:
                shortest_path_length = iteration_shortest_path[1]
                all_time_shortest_path = iteration_shortest_path
            self.pheromone *= self.decay
        
        return all_time_shortest_path

    def construct_colony_paths(self, start_node):
        all_paths = []
        for _ in range(self.n_ants):
            path = self.construct_path(start_node)  # Start from the given start_node
            all_paths.append((path, self.path_distance(path)))
        return all_paths

    def construct_path(self, start_node):
        path = [start_node]
        visited = set()
        visited.add(start_node)
        prev = start_node
        for _ in range(len(self.dist_matrix) - 1):
            move = self.pick_move(self.pheromone[prev], self.dist_matrix[prev], visited)
            path.append(move)
            visited.add(move)
            prev = move
        path.append(start_node)  # Complete the cycle
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0  # 设置已经访问过的节点的概率为 0

        with np.errstate(divide='ignore', invalid='ignore'):
            probabilities = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
            probabilities = np.nan_to_num(probabilities, nan=0.0, posinf=0.0, neginf=0.0)
            sum_probabilities = probabilities.sum()
            if sum_probabilities == 0:
                return np.random.choice(self.all_inds, 1)[0]  # 如果所有路径的概率为 0，随机选择一个未访问的节点
            probabilities /= sum_probabilities

        move = np.random.choice(self.all_inds, p=probabilities)
        return move

    def path_distance(self, path):
        total_dist = 0
        for i in range(len(path) - 1):
            total_dist += self.dist_matrix[path[i], path[i + 1]]
        return total_dist

    def spread_pheromone(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in zip(path[:-1], path[1:]):
                self.pheromone[move] += 1.0 / dist

coord = [0.6683, 0.2536, 0.6195, 0.2634, 0.4, 0.4439, 0.2439, 0.1463, 0.1707, 0.2293,
         0.2293, 0.761, 0.5171, 0.9414, 0.8732, 0.6536, 0.6878, 0.5219, 0.8488, 0.3609]
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

# 计算两点之间的距离矩阵
dist_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        dist_matrix[i, j] = dist_matrix[j, i] = np.linalg.norm(coord[i] - coord[j])

# 运行蚁群算法，遍历所有可能的起点
best_path_overall = None
shortest_path_length_overall = np.inf

for start_node in range(n):
    ant_colony = AntColony(dist_matrix, n_ants=10, n_best=3, n_iterations=100, decay=0.95, alpha=1, beta=2)
    shortest_path, shortest_path_length = ant_colony.run(start_node)
    
    if shortest_path_length < shortest_path_length_overall:
        shortest_path_length_overall = shortest_path_length
        best_path_overall = shortest_path

# 输出最佳路径
print(f"总体最短路径: {best_path_overall}")
print(f"总体最短路径长度: {shortest_path_length_overall}")

# 可视化最短路径
plt.scatter(coord[:, 0], coord[:, 1], color='w', edgecolors='b')
for i in range(len(best_path_overall)):
    plt.text(coord[best_path_overall[i], 0] + 0.01, coord[best_path_overall[i], 1] + 0.01, str(best_path_overall[i]), fontsize=12)

for i in range(len(best_path_overall) - 1):
    xi = coord[best_path_overall[i], 0]
    yi = coord[best_path_overall[i], 1]
    xj = coord[best_path_overall[i + 1], 0]
    yj = coord[best_path_overall[i + 1], 1]
    plt.plot([xi, xj], [yi, yj], color='r')

plt.plot([coord[best_path_overall[-1], 0], coord[best_path_overall[0], 0]],
         [coord[best_path_overall[-1], 1], coord[best_path_overall[0], 1]], color='r')  # 闭合路径
plt.show()