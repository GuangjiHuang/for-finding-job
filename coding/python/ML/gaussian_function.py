import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def gaussian1D(x, mean, std):
    exp_val = - (x - mean) ** 2 / (2 * std ** 2)
    fac = 1 / (std * math.sqrt(2*math.pi))
    ret = fac * np.exp(exp_val)
    return ret

def gaussian2D(x, y, x_m, y_m, std):
    exp_val = - ((x - x_m) ** 2 + (y - y_m) ** 2) / (2 * std ** 2)
    fac = 1 / (std**2 * 2 * math.pi)
    ret = fac * np.exp(exp_val)
    return ret


# get the gaussian value
#x, y = np.mgrid[-5:5:200j, -5:5:200j]
#ret = gaussian2D(x, y, 0, 0, 1)
#print(ret)
## draw the figure
#fig = plt.figure()
#ax = Axes3D(fig)
#ax.plot_surface(x, y, ret, rstride=1, cstride=1, cmap='rainbow', alpha=0.0)
#plt.show()
# draw the picture
#fig = plt.figure()
#plt.plot(x, y)
#plt.show()


x,y = np.mgrid[-5:5:200j,-5:5:200j]
sigma = 2
z = 1/(2 * np.pi * (sigma**2)) * np.exp(-(x**2+y**2)/(2 * sigma**2))


fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='rainbow',alpha = 0.9)

plt.show()
