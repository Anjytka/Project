# -*- coding: utf-8 -*-
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
from tabulate import tabulate
from kalman import *
import csv
import numpy as np
from progecting import *
from moving_average import *
from viewer import *
from sys import stdin

gravity = 9.81

types=('acc','motionAcc')
for i in types:
	exec('{}="{}"'.format(i,i))

"""Get acceleration columns indexes by their names"""
def _get_acc_indexes(t, arr):
	colNames = {}
	colNames[acc] = ["loggingSample","accelerometerTimestamp_sinceReboot","accelerometerAccelerationX","accelerometerAccelerationY","accelerometerAccelerationZ"]
	colNames[motionAcc] = ["loggingSample","motionTimestamp_sinceReboot","motionUserAccelerationX","motionUserAccelerationY","motionUserAccelerationZ"]
	res = []
	i = 0
	for elem in arr:
		if elem in colNames[t]:
			res.append(i)
		i +=1
	return res

"""Get rotation columns indexes by their names"""
def _get_gyr_indexes(arr):
	print 
	colNames = ["loggingSample","motionTimestamp_sinceReboot","motionYaw","motionRoll","motionPitch"]
	res = []
	i = 0
	for elem in arr:
		if elem in colNames:
			res.append(i)
		i +=1
	return res

def _convert_str_to_float_data(data, data_type = 0):	
	t = [row[1] for row in data[1:]]

	massData = []

	t = [float(i) for i in t]
	if data_type == 0:
		x = [row[2] for row in data[1:]]
		y = [row[3] for row in data[1:]]
		z = [row[4] for row in data[1:]]
		massData.append([float(i)*gravity for i in x])
		massData.append([float(i)*gravity for i in y])
		massData.append([float(i)*gravity for i in z])
	if data_type == 1:
		yaw = [row[2] for row in data[1:]]
		roll = [row[3] for row in data[1:]]
		pitch = [row[4] for row in data[1:]]
		massData.append([float(i) for i in yaw])
		massData.append([float(i) for i in roll])
		massData.append([float(i) for i in pitch])
	return (t, np.array(massData))

def data_processor():
	print "Введите путь к файлу:"
	path = stdin.readline().strip()
	with open(path, 'rb') as inputFile:
		reader = csv.reader(inputFile,  delimiter = ',')
		dataAcc = []
		dataGyr = []
		rotIndexes = []
		accIndexes = []
		for (i,row) in enumerate(reader):
			r = np.array(row)
			if i == 0:
				accIndexes = _get_acc_indexes(motionAcc, r)
				gyrIndexes = _get_gyr_indexes(r)
			dataAcc.append(r[accIndexes].tolist())
			dataGyr.append(r[gyrIndexes].tolist())
		(accT, accXYZ)= _convert_str_to_float_data(dataAcc, 0)
		(gyrT, gyrXYZ)= _convert_str_to_float_data(dataGyr, 1)

		accXYZ = np.vstack((accXYZ))
		gyrXYZ = np.vstack((accXYZ))
		print accXYZ[:,0]
		accXYZ = rotateAccels(accXYZ, gyrXYZ, gyrT)

		"""Без фильтров"""
		coord_wo = []
		for i in range(len(accXYZ)):
			coord_wo.append(calc_coord(accXYZ[i],accT))

		"""Простое СС"""
		print "Введите размер окна для простого скользящего среднего:"
		w = int(stdin.readline().strip())
		coord_ma = []
		for i in range(len(accXYZ)):
			coord_ma.append(calc_coord_ma(accXYZ[i], accT, w))

		"""Экспоненциальное взвешенное СС"""
		print "Введите размер окна для экспоненциального взвешенного скользящего среднего:"
		w = int(stdin.readline().strip())
		coord_ema = []
		for i in range(len(accXYZ)):
			coord_ma.append(calc_coord_ema(accXYZ[i], accT, w))
		
		"""Фильтр Калмана"""
		coord_Kalm = []
		speed_Kalm = []
		for i in range(len(accXYZ)):
			res = calc_kalman(accXYZ[i], accT)
			coord_Kalm.append(res[0])
			speed_Kalm.append(res[1])

		"""Фильтр Калмана + Экспоненциальное взвешенное СС"""
		coord_Kalm_ema = []
		count = 100
		for i in range(len(coord_Kalm)):
			coord_Kalm_ema.append(movingExpAverage(coord_Kalm[i],count))

		print "Введите 'y', чтобы вывести 2D график для данных без фильтра"
		val = stdin.readline().strip()
		if (val == "y"):
			show2d_coord_by_wo(coord_wo)

		print "Введите 'y', чтобы вывести 2D график для данных отфильтрованных простым скользящим средним"
		val = stdin.readline().strip()
		if (val == "y"):
			show2d_coord_by_ma(coord_ma)
		
		print "Введите 'y', чтобы вывести 2D график для данных отфильтрованных экспоненциальным взвешенным скользящим средним"
		val = stdin.readline().strip()
		if (val == "y"):
			show2d_coord_by_ema(coord_ema)

		print "Введите 'y', чтобы вывести 2D график для данных отфильтрованных фильтром Калмана"
		val = stdin.readline().strip()
		if (val == "y"):
			show2d_coord_by_kalm(coord_Kalm)
		
		print "Введите 'y', чтобы вывести 3D график для данных без фильтра"
		val = stdin.readline().strip()
		if (val == "y"):
			show3d(coord_wo)
		
		print "Введите 'y', чтобы вывести 3D график для данных отфильтрованных простым скользящим средним"
		val = stdin.readline().strip()
		if (val == "y"):
			show3d(coord_ma)
		
		print "Введите 'y', чтобы вывести 3D график для данных отфильтрованных экспоненциальным взвешенным скользящим средним"
		val = stdin.readline().strip()
		if (val == "y"):
			show3d(coord_ema)

		print "Введите 'y', чтобы вывести 3D график для данных отфильтрованных фильтром Калмана"
		val = stdin.readline().strip()
		if (val == "y"):
			show3d(coord_Kalm)

		print "Введите 'y', чтобы вывести 3D график для данных отфильтрованных фильтром Калмана и после экспоненциальным взвешенным скользящим средним"
		val = stdin.readline().strip()
		if (val == "y"):
			show3d_kalman_vs_ema(coord_Kalm, coord_Kalm_ema)
	
		plt.show()

if __name__ == "__main__":
	data_processor()




