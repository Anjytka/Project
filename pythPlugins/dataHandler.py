import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys

data = dict(dt = float(0),dx = float(0),dy = float(0),dz = float(0))
# vals = dict(T = 0,ax = 0,ay = 0,az = 0)
prevT = float(0)
first = True
second = True
# prevT = "prevT"
dt = "dt"
dx = "dx"
dy = "dy"
dz = "dz"
vx = float(0)
vy = float(0)
vz = float(0)
ax = float(0)
ay = float(0)
az = float(0)


# T = "T"
# ax = "ax"
# ay = "ay"
# az = "az"


def getCoords(vals):
	global first, prevT, vx, vy, vz, ax, ay, az
	if (first):
		prevT = float(vals[0])
		print "prevT = ", prevT
		first = False
		return data

##	data[dt] = round(float((long((vals[0])) - prevT)) / 1000, 3)
	# data[dt] = long(vals[0]) / 1000
	# prevT = long(vals[0]) / 1000

	# print " vx : ",vx,"vy : ",vy,"vz : ",vz
	# data[dx] = round(data[dx] + vx*data[dt] + float(vals[1])*pow(data[dt],2)/2, 3)
	# data[dy] = round(data[dy] + vy*data[dt] + float(vals[2])*pow(data[dt],2)/2, 3)
	# data[dz] = round(data[dz] + vz*data[dt] + float(vals[3])*pow(data[dt],2)/2, 3)
##	vx1 = vx + float(vals[1])*data[dt]
##	vy1 = vy + float(vals[2])*data[dt]
##	vz1 = vz + float(vals[3])*data[dt]
##	data[dx] = round((pow(vx1,2)-pow(vx,2))/(2*float(vals[1])))
##	data[dy] = round((pow(vy1,2)-pow(vy,2))/(2*float(vals[2])))
##	data[dz] = round((pow(vz1,2)-pow(vz,2))/(2*float(vals[3])))
##	vx = vx1
##	vy = vy1
##	vz = vz1
	data[dt] = float(vals[0]) - prevT
	# vx = vx + (float(vals[1]) + ax)/2 * data[dt]
	# vy = vy + (float(vals[2]) + ay)/2 * data[dt]
	# vz = vz + (float(vals[3]) + az)/2 * data[dt]
	# data[dx] = data[dx] + vx * data[dt]
	# data[dy] = data[dy] + vy * data[dt]
	# data[dz] = data[dz] + vz * data[dt]

	vx = vx + float(vals[1]) * data[dt]
	vy = vy + float(vals[2]) * data[dt]
	vz = vz + float(vals[3]) * data[dt]
	data[dx] = data[dx] + vx * data[dt] + float(vals[1]) * pow(data[dt],2)/2
	data[dy] = data[dy] + vy * data[dt] + float(vals[2]) * pow(data[dt],2)/2
	data[dz] = data[dz] + vz * data[dt] + float(vals[3]) * pow(data[dt],2)/2


	# ax = float(vals[1])
	# ay = float(vals[2])
	# az = float(vals[3])
	prevT = float(vals[0])
	# velocity[index] += (event.values[index] + last_values[index])/2 * dt;
 #    position[index] += velocity[index] * dt;

	return data

f = open("text.txt", 'r')
f2 = open("res.txt", "w")
lines = f.readlines()
for line in lines:
	vals = line.split(",")
	vals = [v.strip() for v in vals]
	if first:
		getCoords(vals)
	else:
		coords = getCoords(vals)
		f2.write(str(coords[dx])+","+str(coords[dy])+","+str(coords[dz])+"\n")
		print coords


# dataArr = np.genfromtxt("res.txt", delimiter=",", dtype=(float, float, float))
# x = dataArr[:,0]
# y = dataArr[:,1]
# z = dataArr[:,2]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, y, -z, zdir='z', c= 'red')
# plt.savefig("demo.png")
# s = lines[0].split(",")
# s = [v.strip() for v in s]
# coords = getCoords(s)
# print coords

# print data[prevT]
# print lines[len(s)-1]