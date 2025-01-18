import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
from numpy import random
import itertools

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
        
min_result = np.inf
min_path = list(range(n))
path = list(range(n))
N = 10000000
for k in range(N):
    result = 0
    shuffle(path)
    for l in range(n-2):
        result = result + d[path[l], path[l+1]]
    result += d[path[0],path[n-1]]
    if result < min_result:
        min_result = result
        min_path = path
min_path.append(min_path[0])
print("最短路径长度为：", min_result)
print("最短路径为：", min_path)
for i in range(n):
    j = i + 1
    xi = coord[min_path[i], 0]
    yi = coord[min_path[i], 1]
    xj = coord[min_path[j], 0]
    yj = coord[min_path[j], 1]
    plt.plot([xi, xj], [yi, yj])