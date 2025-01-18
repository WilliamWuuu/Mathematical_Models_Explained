# 埃尔米特插值
from scipy.interpolate import KroghInterpolator as ki
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

np.set_printoptions(suppress=True)  # 不适用科学计数法

x = np.linspace(-np.pi, np.pi, 7, endpoint=True)  # 在[-Π,Π]上生成7个数，包含Π
y = np.sin(x)
new_x = np.array(np.arange(min(x), max(x), 0.1))  # 从[-Π,Π]上每隔0.1取一个数，作为待插坐标
interpolant = ki(x, y)  #构造Hermite方法
sin_x = np.array(np.arange(-np.pi, np.pi, 0.01))  # 用于绘制三角函数sin

plt.style.use(["science", "no-latex"])
plt.figure(figsize=(10, 8))
plt.plot(new_x, interpolant(new_x), '--', label='Hermite Interpolation')  # 绘制Hermite插值图
plt.scatter(x, np.sin(x), label='Sample point')  # 原始样本点
plt.plot(sin_x, np.sin(sin_x),  label='sin(x)')  # 绘制三角函数图sin
plt.legend(fontsize=13)  # 显示图例

plt.show()
