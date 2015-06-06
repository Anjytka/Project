# # x = (1, 0, 0)
# # y = (0, 1, 0)
# # z = (0, 0, 1)
# # o = (0, 0, 0)
# # -*- coding: utf-8 -*-
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
# from itertools import product, combinations

# # ax = fig.gca(projection='3d')


# """!!!"""
# 	# #draw cube
# 	# r = [-1, 1]
# 	# for s, e in combinations(np.array(list(product(r,r,r))), 2):
# 	#     if np.sum(np.abs(s-e)) == r[1]-r[0]:
# 	#         ax.plot3D(*zip(s,e), color="b")

# 	# #draw sphere
# 	# u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
# 	# x=np.cos(u)*np.sin(v)
# 	# y=np.sin(u)*np.sin(v)
# 	# z=np.cos(v)
# 	# ax.plot_wireframe(x, y, z, color="r")

# 	# #draw a point
# 	# ax.scatter([0],[0],[0],color="g",s=100)

# #draw a vector
# from matplotlib.patches import FancyArrowPatch
# from mpl_toolkits.mplot3d import proj3d

# class Arrow3D(FancyArrowPatch):
#     def __init__(self, xs, ys, zs, *args, **kwargs):
#         FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
#         self._verts3d = xs, ys, zs

#     def draw(self, renderer):
#         xs3d, ys3d, zs3d = self._verts3d
#         xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
#         self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
#         FancyArrowPatch.draw(self, renderer)

# x = Arrow3D([0,1],[0,0],[0,0], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
# y = Arrow3D([0,0],[0,1],[0,0], mutation_scale=20, lw=1, arrowstyle="-|>", color="g")
# z = Arrow3D([0,0],[0,0],[0,1], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")

# fig = plt.figure(1)
# ax1 = fig.add_subplot(2, 2, 1, projection='3d') 
# ax1.set_aspect("equal")
# # ax1.set_axis_off()
# ax1.add_artist(x)
# ax1.add_artist(y)
# ax1.add_artist(z)
# ax1.view_init(elev=15., azim=10)

# ax2 = fig.add_subplot(2, 2, 2, projection='3d') 
# ax2.set_aspect("equal")
# # ax2.set_axis_off()
# ax2.add_artist(x)
# ax2.add_artist(y)
# ax2.add_artist(z)
# ax2.view_init(elev=15., azim=100)

# ax3 = fig.add_subplot(2, 2, 3, projection='3d') 
# ax3.set_aspect("equal")
# # ax3.set_axis_off()
# ax3.add_artist(x)
# ax3.add_artist(y)
# ax3.add_artist(z)
# ax3.view_init(elev=105., azim=10)

# ax4 = fig.add_subplot(2, 2, 4, projection='3d') 
# ax4.set_aspect("equal")
# # ax4.set_axis_off()
# ax4.add_artist(x)
# ax4.add_artist(y)
# ax4.add_artist(z)
# ax4.view_init(elev=105., azim=100)

# plt.subplots_adjust(bottom=0.15)
# plt.show()

import numpy as np
import math
q = np.array([1, 2, 3], dtype=np.float64, copy=True)
print q
n = np.dot(q, q)
print n
q *= math.sqrt(2.0 / n)
print q
q = np.outer(q, q)
print q
print range(5, 7)
a = [6, 7, 8, 4, 5]
print "a=", a[1:]


