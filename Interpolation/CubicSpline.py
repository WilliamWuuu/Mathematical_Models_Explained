# 三次样条插值
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

x = np.linspace(-np.pi, np.pi, 7, endpoint=True)
y = np.sin(x)
xx = np.arange(min(x), max(x), 0.1)
_, ax = plt.subplots(figsize=(10, 8))
ax.scatter(x, y, label='Sample point')
# cubic：三次样条插值
spline = interp1d(x, y, kind='cubic')  
ax.plot(xx, spline(xx), label='Spline')
ax.plot(xx, np.sin(xx), '--', label='sin(x)')
plt.legend(fontsize=13, loc='best')

plt.show()