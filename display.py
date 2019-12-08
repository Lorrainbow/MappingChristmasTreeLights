import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

data = np.loadtxt('xyz.csv',delimiter=',', skiprows=1).T

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs=data[0,:], ys=data[1,:], zs=-data[2,:])
ax.auto_scale_xyz(*[[-200,200]]*3)
plt.show()

