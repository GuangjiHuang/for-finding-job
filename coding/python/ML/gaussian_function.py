import numpy as np
import math
import matplotlib.pyplot as plt

def gaussian1D(x, mean, std):
    exp_val = - (x - mean) ** 2 / (2 * std ** 2)
    fac = 1 / (std * math.sqrt(2*math.pi))
    ret = fac * np.exp(exp_val)
    return ret

def gaussian2D(mean, std):
    pass

# get the gaussian value
x = np.arange(-2, 2, 0.01)
y = gaussian1D(x, 0, 1)
# draw the picture
fig = plt.figure()
plt.plot(x, y)
plt.show()


print(y)

