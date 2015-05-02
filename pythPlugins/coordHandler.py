# -*- coding: utf-8 -*-
import numpy as np
from kalmanMatrix import *
"""
data:
	0   1   2   3
	t	x	y 	z
0   .   .   .   .
1   .   .   .   .
2   .   .   .
"""
def countCoodr(data):
	# res = [[" ","Ax","Vx","X",]]
	# dt = vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
		# dt = data[1][0] - data[0][0]
		# vxPr = data[1][1]*dt
		# vyPr = data[1][2]*dt
		# vzPr = data[1][3]*dt
		# x = [0]
		# y = [0]
		# z = [0]
		# for (i,item) in enumerate(data[2:]):
		# 	x.append(x[i] + vxPr*dt + item[1]*pow(dt,2)/2)
		# 	y.append(y[i] + vyPr*dt + item[2]*pow(dt,2)/2)
		# 	z.append(z[i] + vzPr*dt + item[3]*pow(dt,2)/2)
		# 	dt = item[0] - dt - data[0][0]
		# 	vxPr = vxPr + item[1]*dt
		# 	vyPr = vyPr + item[2]*dt
		# 	vzPr = vzPr + item[3]*dt

	# dt = vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
		# dt = data[1][0] - data[0][0]
		# vxPr = data[1][1]*dt
		# vyPr = data[1][2]*dt
		# vzPr = data[1][3]*dt
		# x = [0]
		# y = [0]
		# z = [0]
		# xPr = 0
		# yPr = 0
		# zPr = 0
		# for (i,item) in enumerate(data[2:]):
		# 	print "ZERO", i, xPr, yPr, zPr
		# 	x.append(xPr + vxPr*dt + item[1]*pow(dt,2)/2)
		# 	y.append(yPr + vyPr*dt + item[2]*pow(dt,2)/2)
		# 	z.append(zPr + vzPr*dt + item[3]*pow(dt,2)/2)
		# 	xPr = x[i]
		# 	yPr = y[i]
		# 	zPr = z[i]
		# 	print "AFTE", i, xPr, yPr, zPr
		# 	dt = item[0] - dt - data[0][0]
		# 	vxPr = vxPr + item[1]*dt
		# 	vyPr = vyPr + item[2]*dt
		# 	vzPr = vzPr + item[3]*dt

	# dt = vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
		# dt = data[1][0] - data[0][0]
		# vxPr = (data[1][1] - data[0][1])*dt
		# vyPr = (data[1][2] - data[0][2])*dt
		# vzPr = (data[1][3] - data[0][3])*dt
		# axPr = data[1][1]
		# ayPr = data[1][2]
		# azPr = data[1][3]
		# x = [0]
		# y = [0]
		# z = [0]
		# xPr = yPr = zPr = 0
		# for (i,item) in enumerate(data[2:]):
		# 	# print "ZERO", i, xPr, yPr, zPr
		# 	x.append(xPr + vxPr*dt + (item[1] - axPr)*pow(dt,2)/2)
		# 	y.append(yPr + vyPr*dt + (item[2] - ayPr)*pow(dt,2)/2)
		# 	z.append(zPr + vzPr*dt + (item[3] - azPr)*pow(dt,2)/2)
		# 	xPr = x[i]
		# 	yPr = y[i]
		# 	zPr = z[i]
		# 	# print "AFTE", i, xPr, yPr, zPr
		# 	dt = item[0] - dt - data[0][0]
		# 	vxPr = vxPr + (item[1] - axPr)*dt
		# 	vyPr = vyPr + (item[2] - ayPr)*dt
		# 	vzPr = vzPr + (item[3] - azPr)*dt
		# 	axPr = item[1]
		# 	ayPr = item[2]
		# 	azPr = item[3]

	"""Вычитание ускорений"""
	# dt = vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
	# axPr = data[0][1]
	# ayPr = data[0][2]
	# azPr = data[0][3]
	# x = [0]
	# y = [0]
	# z = [0]
	# xPr = yPr = zPr = 0
	# for (i,item) in enumerate(data[1:]):
	# 	dt = item[0] - dt - data[0][0]
	# 	dax = (item[1] - axPr)
	# 	day = (item[2] - ayPr)
	# 	daz = (item[3] - azPr)
	# 	vxPr = vxPr + dax*dt
	# 	vyPr = vyPr + day*dt
	# 	vzPr = vzPr + daz*dt
	# 	# print "ZERO", i, xPr, yPr, zPr
	# 	x.append(xPr + vxPr*dt + dax*pow(dt,2)/2)
	# 	y.append(yPr + vyPr*dt + day*pow(dt,2)/2)
	# 	z.append(zPr + vzPr*dt + daz*pow(dt,2)/2)
		
	# 	# x.append(xPr + vxPr*dt + (vx - vxPr)*dt/2)
	# 	# y.append(yPr + vyPr*dt + (vy - vyPr)*dt/2)
	# 	# z.append(zPr + vzPr*dt + (vz - vzPr)*dt/2)
	# 	# res.append()

	# 	xPr = x[i]
	# 	yPr = y[i]
	# 	zPr = z[i]
	# 	# print "AFTE", i, xPr, yPr, zPr
	# 	axPr = item[1]
	# 	ayPr = item[2]
	# 	azPr = item[3]

	"""Физические формулы"""
	# dt = vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
	# axPr = data[0][1]
	# ayPr = data[0][2]
	# azPr = data[0][3]
	# x = [0]
	# y = [0]
	# z = [0]
	# xPr = yPr = zPr = 0
	# for (i,item) in enumerate(data[1:]):
	# 	dt = item[0] - dt - data[0][0]
	# 	ax = item[1] + axPr
	# 	ay = item[2] + ayPr
	# 	az = item[3] + azPr
	# 	vx = vxPr + ax*dt/2
	# 	vy = vyPr + ay*dt/2
	# 	vz = vzPr + az*dt/2
	# 	# print "ZERO", i, xPr, yPr, zPr
	# 	x.append(xPr + (vx + vxPr)*dt/2)
	# 	y.append(yPr + (vy + vyPr)*dt/2)
	# 	z.append(zPr + (vz + vzPr)*dt/2)

	"""Физические формулы"""
	# vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
	# tPr = data[0][0]
	# axPr = data[0][1]
	# ayPr = data[0][2]
	# azPr = data[0][3]
	# x = [0]
	# y = [0]
	# z = [0]
	# xPr = yPr = zPr = 0
	# for (i,item) in enumerate(data[1:]):
	# 	dt = item[0] - tPr
	# 	ax = item[1] #+ (item[1] - axPr)/2
	# 	ay = item[2] #+ (item[2] - ayPr)/2
	# 	az = item[3] #+ (item[3] - azPr)/2
	# 	vx = vxPr + ax*dt
	# 	vy = vyPr + ay*dt
	# 	vz = vzPr + az*dt
	# 	# print "ZERO", i, xPr, yPr, zPr
	# 	x.append(xPr + (vx)*dt + ax*pow(dt,2)/2)
	# 	y.append(yPr + (vy)*dt + ay*pow(dt,2)/2)
	# 	z.append(zPr + (vz)*dt + az*pow(dt,2)/2)

	# # 	# res.append()

	# 	xPr = x[i]
	# 	yPr = y[i]
	# 	zPr = z[i]
	# 	vxPr = vx
	# 	vyPr = vy
	# 	vzPr = vz
	# 	tPr = item[0]
	# 	# print "AFTE", i, xPr, yPr, zPr
	# 	axPr = item[1]
	# 	ayPr = item[2]
	# 	azPr = item[3]

	"""Физические формулы с накоплением v и фильтрацией"""
	vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
	tPr = data[0][0]
	axPr = data[0][1]
	ayPr = data[0][2]
	azPr = data[0][3]
	vx = [0]
	vy = [0]
	vz = [0]
	x = [0]
	y = [0]
	z = [0]
	xPr = yPr = zPr = 0
	for (i,item) in enumerate(data[1:]):
		dt = item[0] - tPr
		ax = item[1] #+ (item[1] - axPr)/2
		ay = item[2] #+ (item[2] - ayPr)/2
		az = item[3] #+ (item[3] - azPr)/2
		vx.append(vxPr + ax*dt)
		vy.append(vyPr + ay*dt)
		vz.append(vzPr + az*dt)
		# print "ZERO", i, xPr, yPr, zPr
		# print vxPr + ax*dt, vx[i-1], vx[i], vx[i+1]
		x.append(xPr + (vx[i+1])*dt + ax*pow(dt,2)/2)
		y.append(yPr + (vy[i+1])*dt + ay*pow(dt,2)/2)
		z.append(zPr + (vz[i+1])*dt + az*pow(dt,2)/2)

	# 	# res.append()

		xPr = x[i+1]
		yPr = y[i+1]
		zPr = z[i+1]
		vxPr = vx[i+1]
		vyPr = vy[i+1]
		vzPr = vz[i+1]
		tPr = item[0]
		# print "AFTE", i, xPr, yPr, zPr
		axPr = item[1]
		ayPr = item[2]
		azPr = item[3]

	# vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
	# tPr = data[0][0]
	# axPr = data[0][1]
	# ayPr = data[0][2]
	# azPr = data[0][3]
	# x = []
	# y = []
	# z = []
	# xPr = yPr = zPr = 0
	# averAx = averAy = averAz = 0
	# for (i,item) in enumerate(data[1:]):
		
	# 	dt = item[0] - tPr
	# 	ax = item[1] - abs(data[0][1])# + (item[1] - axPr)/2
	# 	ay = item[2] - abs(data[0][2])# + (item[2] - ayPr)/2
	# 	az = item[3] - abs(data[0][3])# + (item[3] - azPr)/2
	# 	averAx += ax
	# 	averAy += ay
	# 	averAz += az
	# 	vx = vxPr + (ax + axPr)/2*dt
	# 	vy = vyPr + (ay + ayPr)/2*dt
	# 	vz = vzPr + (az + azPr)/2*dt
	# 	# print "ZERO", i, xPr, yPr, zPr
	# 	x.append(xPr + (vx + vxPr)/2*dt + (ax + axPr)/2*pow(dt,2))
	# 	y.append(yPr + (vy + vyPr)/2*dt + (ay + ayPr)/2*pow(dt,2))
	# 	z.append(zPr + (vz + vzPr)/2*dt + (az + azPr)/2*pow(dt,2))

	# 	# res.append()
	# 	# print x[i], x[-1]
	# 	xPr = x[-1]
	# 	yPr = y[-1]
	# 	zPr = z[-1]
	# 	vxPr = vx
	# 	vyPr = vy
	# 	vzPr = vz
	# 	tPr = item[0]
	# 	# print "AFTE", i, xPr, yPr, zPr
	# 	axPr = item[1]
	# 	ayPr = item[2]
	# 	azPr = item[3]

	# dt = vxPr = vyPr = vzPr = xPr = yPr = zPr = 0
		# dt = data[1][0] - data[0][0]
		# axPr = data[1][1]
		# ayPr = data[1][2]
		# azPr = data[1][3]
		# x = [0]
		# y = [0]
		# z = [0]
		# for (i,item) in enumerate(data[2:]):
		# 	vxPr = (axPr+item[1]) * dt/2
		# 	vyPr = (ayPr+item[2]) * dt/2
		# 	vzPr = (azPr+item[3]) * dt/2
		# 	x.append(x[i] + vxPr*dt + item[1]*pow(dt,2)/2)
		# 	y.append(y[i] + vyPr*dt + item[1]*pow(dt,2)/2)
		# 	z.append(z[i] + vzPr*dt + item[1]*pow(dt,2)/2)
		# 	dt = item[0] - dt - data[0][0]
			
		# print data[0]
		# print vx0, vy0, vz0
	# print averAx/(len(data)-1)
	# print averAy/(len(data)-1)
	# print averAz/(len(data)-1)

	print x[-1]
	print y[-1]
	print z[-1]
	return [x, y, z]



def calcVelocity(data):
	tPr = data[0][0]
	axPr = data[0][1]
	ayPr = data[0][2]
	azPr = data[0][3]
	vx = [0]
	vy = [0]
	vz = [0]
	for (i, item) in enumerate(data[1:]):
		dt = item[0] - tPr
		# vx.append(vx[i] + item[1]*dt)
		# vy.append(vy[i] + item[2]*dt)
		# vz.append(vz[i] + item[3]*dt)
		vx.append(vx[i] + (axPr + item[1])*dt/2)
		vy.append(vy[i] + (ayPr + item[2])*dt/2)
		vz.append(vz[i] + (azPr + item[3])*dt/2)
		tPr = item[0]
		axPr = item[1]
		ayPr = item[2]
		azPr = item[3]
	vx = calcKalman(vx, 0)
	vy = calcKalman(vy, 0)
	vz = calcKalman(vz, 0)
	fig = plt.figure(1)
	ax = fig.gca(projection='3d')
	ax.plot(vx, vy, vz, color="b")
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	# ax.plot(coordsStart[0], coordsStart[1], coordsStart[2], color="r")

	return [vx, vy, vz]



def calcCoords(dataA, dataV):
	tPr = dataA[0][0]
	x = [0]
	y = [0]
	z = [0]
	for (i, item) in enumerate(dataA[1:]):
		dt = item[0] - tPr
		# x.append(x[i] + dataV[0][i+1]*dt + item[1]*pow(dt, 2)/2)
		# y.append(y[i] + dataV[1][i+1]*dt + item[2]*pow(dt, 2)/2)
		# z.append(z[i] + dataV[2][i+1]*dt + item[3]*pow(dt, 2)/2)
		
		x.append(x[i] + (dataV[0][i+1] + dataV[0][i])*dt/2)
		y.append(y[i] + (dataV[1][i+1] + dataV[1][i])*dt/2)
		z.append(z[i] + (dataV[2][i+1] + dataV[2][i])*dt/2)
		tPr = item[0]
	x = calcKalman(x, 0)
	y = calcKalman(y, 0)
	z = calcKalman(z, 0)

	fig = plt.figure(2)
	ax = fig.gca(projection='3d')
	ax.plot(x, y, z, color="b")
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	print x[-1]
	print y[-1]
	print z[-1]

	# ax.plot(coordsStart[0], coordsStart[1], coordsStart[2], color="r")

	return [x, y, z]

