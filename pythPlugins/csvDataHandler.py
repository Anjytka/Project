# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib as plt
from tabulate import tabulate
from movingAverage import *
from kalmanMatrix import *
from coordHandler import *
import transformations as tf
# import coordHandler as cdHlr


gravity = 9.81

types=('acc','motionAcc')
for i in types:
	exec('{}="{}"'.format(i,i))

"""Get acceleration columns indexes by their names"""
def get_acc_indexes(t, arr):
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
def  get_rot_indexes(arr):
	print 
	colNames = ["loggingSample","motionTimestamp_sinceReboot","motionYaw","motionRoll","motionPitch"]
	res = []
	i = 0
	for elem in arr:
		if elem in colNames:
			res.append(i)
		i +=1
	return res

def convert_str_to_float_data(data, dataType = 0):	
	t = [row[1] for row in data[1:]]
	x = [row[2] for row in data[1:]]
	y = [row[3] for row in data[1:]]
	z = [row[4] for row in data[1:]]

	t = [float(i) for i in t]
	x = [float(i)*gravity for i in x] if dataType else [float(i) for i in x]
	y = [float(i)*gravity for i in y] if dataType else [float(i) for i in y]
	z = [float(i)*gravity for i in z] if dataType else [float(i) for i in z]
	return (t, [x, y, z])

def get_quaternions_from_euler(rotXYZ):
	result = []
	rotXYZ = np.array(rotXYZ)
	for i in range(len(rotXYZ[0])):
		quaternion = tf.quaternion_from_euler(rotXYZ[:,i][1], rotXYZ[:,i][2], rotXYZ[:,i][0])
		result.append(quaternion)
	return result

# with open('streight4m_with_motion.csv', 'rb') as inputFile, open('output.csv', 'rwb') as outputFile:
with open('Data/Y-X20-50.csv', 'rb') as inputFile, open('Data/output.csv', 'rwb') as outputFile:
	reader = csv.reader(inputFile,  delimiter = ',')
	writer = csv.writer(outputFile, delimiter = ',')
	dataAcc = []
	dataRot = []
	rotIndexes = []
	accIndexes = []
	for (i,row) in enumerate(reader):
		a = np.array(row)
		if i == 0:
			accIndexes = get_acc_indexes(motionAcc, a)
			rotIndexes =  get_rot_indexes(a)
			print rotIndexes
		dataAcc.append(a[accIndexes].tolist())
		dataRot.append(a[rotIndexes].tolist())

	# print tabulate(dataAcc[1:], headers=dataAcc[0],floatfmt=".16f")
	# print tabulate(dataRot[1:], headers=dataRot[0],floatfmt=".16f")

	(accT, [accX, accY, accZ])= convert_str_to_float_data(dataAcc, 1)
	(rotT, rotXYZ)= convert_str_to_float_data(dataRot, 0)

	"""Kalman acceleration filtering"""
	accX = calcKalman(accX, 1)
	accY = calcKalman(accY, 2)
	accZ = calcKalman(accZ, 3)
	# plt.show()
	

	"""Rotate acceleration vectors"""
	rotQuaternions = get_quaternions_from_euler(rotXYZ)
	print "Quaternions"
	print rotQuaternions

	"""Example to check if movingAverage works correct
		count = 3 
		exampleArr = [1,0,1,2,-1,2,0,1,5,10,5,1,2,-2,0,-1,2,3,6,9,12,9,6,3,2,1,0,-1,-1,0,0,1,2,1,1,1,2]
		exampleArr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
		array = movAver.movingAverage(exampleArr,count)
		array = movingAverage(exampleArr,count)
		arrayNew = []
		for i in range(len(array)):
			arrayNew.append([float(accT[count-1+i]),float(array[i])])
		print tabulate(arrayNew,headers=['t','Ax'],floatfmt=".16f")"""

	"""Moving Average

		count = 20
		accNewX = movingAverage(accX, count)
		accNewY = movingAverage(accY, count)
		accNewZ = movingAverage(accZ, count)
		# print len(accX), len(accNewX)"""
	
	"""Prepare data for coordinate counting"""
	dataAccNew = []
	for i in range(len(accX)):
		dataAccNew.append([accT[i], accX[i], accY[i], accZ[i]])
	# tab =  tabulate(dataAccNew,headers=['t','Ax','Ay','Az'],floatfmt=".16f")
	# print tab
	
	countCoodr(dataAccNew)






