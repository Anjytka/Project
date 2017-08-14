# -*- coding: utf-8 -*-
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D

iterator = 1
color = 'rgby'

"""Без фильтров"""
def show2d_coord_by_wo(coords):
	global iterator, color
	plt.figure(int(iterator))
	plt.title('Without filters')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance, meters')
	for i in range(len(coords)):
		plt.plot(coords[i], color[i])
	iterator += 1

"""Простое СС"""
def show2d_coord_by_ma(coords):
	global iterator, color
	plt.figure(int(iterator))
	plt.title('Moving average filter')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance, meters')
	for i in range(len(coords)-1):
		plt.plot(coords[i], color[i])
	iterator += 1

"""Экспоненциальное взвешенное СС"""
def show2d_coord_by_ema(coords):
	global iterator, color
	plt.figure(int(iterator))
	plt.title('Exponential Moving Average filter')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance, meters')
	for i in range(len(coords)-1):
		plt.plot(coords[i], color[i])
	iterator += 1

"""Фильтр Калмана"""
def show2d_coord_by_kalm():
	global iterator, color
	plt.figure(int(iterator))
	plt.title('Kalman filter')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance, meters')
	for i in range(len(coords)-1):
		plt.plot(coords[i], color[i])
	iterator += 1

"""3D"""
def show3d(coords):
	global iterator, color
	fig = plt.figure(int(iterator))
	ax = fig.gca(projection='3d')
	ax.plot(coords[0], coords[1], coords[2], color="b")
	ax.plot([coords[0][-1]], [coords[1][-1]], [coords[2][-1]], 'ro')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	iterator += 1

"""Фильтр Калмана и Экспоненциальное взвешенное СС"""
def show3d_kalman_vs_ema(coordsK, coordsEMA):
	global iterator, color
	fig = plt.figure(int(iterator))
	ax = fig.gca(projection='3d')
	ax.plot(coordsK[0], coordsK[1], coordsK[2], color="b")
	ax.plot(coordsEMA[0], coordsEMA[1], coordsEMA[2], color="r")
	ax.plot([coordsK[0][-1]], [coordsK[1][-1]], [coordsK[2][-1]], 'ro')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	iterator += 1