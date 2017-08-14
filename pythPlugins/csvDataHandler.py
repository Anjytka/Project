# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
from tabulate import tabulate
from movingAverage import *
from kalmanM import *
import kalmanM_without_err as kwoe
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

def  get_quat_indexes(arr):
	print 
	colNames = ["loggingSample","motionTimestamp_sinceReboot","motionQuaternionX","motionQuaternionY","motionQuaternionZ","motionQuaternionW"]
	res = []
	i = 0
	for elem in arr:
		if elem in colNames:
			res.append(i)
		i +=1
	return res

def convert_str_to_float_data(data, data_type = 0):	
	t = [row[1] for row in data[1:]]

	massData = []
	# print "T: ",t
	t = [float(i) for i in t]
	if data_type == 1:
		x = [row[2] for row in data[1:]]
		y = [row[3] for row in data[1:]]
		z = [row[4] for row in data[1:]]
		massData.append([float(i)*gravity for i in x])
		massData.append([float(i)*gravity for i in y])
		massData.append([float(i)*gravity for i in z])

	if data_type == 0:
		yaw = [row[2] for row in data[1:]]
		roll = [row[3] for row in data[1:]]
		pitch = [row[4] for row in data[1:]]
		massData.append([float(i) for i in yaw])
		massData.append([float(i) for i in roll])
		massData.append([float(i) for i in pitch])

	if data_type == 2:
		x = [row[2] for row in data[1:]]
		y = [row[3] for row in data[1:]]
		z = [row[4] for row in data[1:]]
		w = [row[5] for row in data[1:]]
		massData.append([float(i) for i in w])
		massData.append([float(i) for i in x])
		massData.append([float(i) for i in y])
		massData.append([float(i) for i in z])


	return (t, np.array(massData))

#not in use
def get_quaternions_from_euler(rotXYZ):
	result = []
	# rotXYZ = np.array(rotXYZ)
	for i in range(len(rotXYZ[0])):
		# q = tf.quaternion_from_euler(rotXYZ[:,i][0]*(180/np.pi), rotXYZ[:,i][1]*(180/np.pi), rotXYZ[:,i][2]*(180/np.pi))
		q = tf.quaternion_from_euler(rotXYZ[:,i][0], rotXYZ[:,i][1], rotXYZ[:,i][2])
		qmatrix = tf.quaternion_matrix(q)
		if i == 0:
			print("Q: ", q, "\n", qmatrix)
		result.append(qmatrix[0:3,0:3])
		# result.append(q)
	return result

def get_quar_matrix_from_quat(qtXYZ):
	result = []
	print(len(qtXYZ[0]))
	# rotXYZ = np.array(rotXYZ)
	for i in range(len(qtXYZ[0])):
		qmatrix = get_quaternion_matrix(qtXYZ[:,i])
		result.append(qmatrix[0:3,0:3])
		if i == 0:
			print("QW: ", qtXYZ[:,i])
			# print "QM: ", qmatrix[0:3,0:3]
		# result.append(q)
	return result

#fiction
def calc_angles(acc, gyr, time):
	K = 0.06
	dt_mass = [time[i]-time[i-1] for i in range(1, len(time))]
	gyr_x = 0
	gyr_y = 0
	gyr_z = 0
	result = []
	for i in range(len(acc)):
		acc_x = np.arctan(acc[0]/
			np.sqrt(pow(acc[1],2)+pow(acc[2],2)))
		acc_y = np.arctan(acc[1]/
			np.sqrt(pow(acc[0],2)+pow(acc[2],2)))
		acc_z = np.arctan(acc[2]/
			np.sqrt(pow(acc[0],2)+pow(acc[1],2)))
		gyr_x = gyr_x + gyr[0]*dt_mass[i]
		gyr_y = gyr_y + gyr[1]*dt_mass[i]
		gyr_z = gyr_z + gyr[2]*dt_mass[i]
		res_x = (1-K)*gyr_x + K*acc_x
		res_y = (1-K)*gyr_y + K*acc_y
		res_z = (1-K)*gyr_z + K*acc_z
		result.append([res_x, res_y, res_z])
	return result

#fiction
def calc_quaternions(angles):
	result = []
	for i in range(len(angles)):
		a = angles[i]
		qr = np.cos(a[0])*np.cos(a[1])*np.cos(a[2]) - np.sin(a[0])*np.sin(a[1])*np.sin(a[2])
		qi = np.cos(a[0])*np.cos(a[1])*np.sin(a[2]) - np.sin(a[0])*np.sin(a[1])*np.cos(a[2])
		qj = np.cos(a[0])*np.sin(a[1])*np.cos(a[2]) - np.sin(a[0])*np.cos(a[1])*np.sin(a[2])
		qk = np.sin(a[0])*np.cos(a[1])*np.cos(a[2]) - np.cos(a[0])*np.sin(a[1])*np.sin(a[2])
		result.append([qr, qi, qj, qk])
	return result

def get_quaternion_matrix(quaternion):
    q = np.array(quaternion, dtype=np.float64, copy=True)
    q = np.outer(q, q)
    return np.array([
        [1.0-2*q[2, 2]-2*q[3, 3],     2*(q[1, 2]-q[3, 0]),
            2*(q[1, 3]+q[2, 0]), 0.0],
        [    2*(q[1, 2]+q[3, 0]), 1.0-2*q[1, 1]-2*q[3, 3],
            2*(q[2, 3]-q[1, 0]), 0.0],
        [    2*(q[1, 3]-q[2, 0]),     2*(q[2, 3]+q[1, 0]),
            1.0-2*q[1, 1]-2*q[2, 2], 0.0],
        [                    0.0,                     0.0,                     0.0, 1.0]])

# Y-X20-50.csv
# Left_tern_on_90_degrees.csv
# streight4m_with_motion.csv
# Y-1000Fr-50.csv
# Y-400Fr-10startwithmotion.csv
# Y-circleFr-100.csv
# Y-400Fr-100InHand.csv
# Y-400|100_left_turn_on 90_deg.csv
# Do_Nothing_10s_Fr-100.csv
# Do_Nothing_1minFr-100.csv
# Y-DownStairsFr-100.csv
# Y-DownStairsWOturnFr-100.csv
with open('Data/Y-400Fr-100InHand.csv', 'rb') as inputFile:
	reader = csv.reader(inputFile,  delimiter = ',')
	dataAcc = []
	dataRot = []
	dataQuat = []
	rotIndexes = []
	accIndexes = []
	quatIndexes = []
	for (i,row) in enumerate(reader):
		r = np.array(row)
		if i == 0:
			accIndexes = get_acc_indexes(motionAcc, r)
			rotIndexes =  get_rot_indexes(r)
			quatIndexes = get_quat_indexes(r)
		dataAcc.append(r[accIndexes].tolist())
		dataRot.append(r[rotIndexes].tolist())
		dataQuat.append(r[quatIndexes].tolist())

	# print tabulate(dataAcc[1:], headers=dataAcc[0],floatfmt=".16f")
	# print tabulate(dataRot[1:], headers=dataRot[0],floatfmt=".16f")
	# print tabulate(dataQuat[1:], headers=dataQuat[0],floatfmt=".16f")

	(accT, accXYZ)= convert_str_to_float_data(dataAcc, 1)
	(rotT, rotXYZ)= convert_str_to_float_data(dataRot, 0)
	(qtT, qtXYZ)= convert_str_to_float_data(dataQuat, 2)
	# for i in range(len(qtXYZ)):
	# 	print "!!!RES:",qtXYZ[i].tolist()


	accXYZ = np.vstack((accXYZ))

	"""Get quaternion matrix for acceleration vectors"""
	# rotQuaternions = get_quaternions_from_euler(rotXYZ)
	rotQuaternions = get_quar_matrix_from_quat(qtXYZ)
	# for item in rotQuaternions:
	# 	print item

	"""Rotate acceleration"""
	# print rotQuaternions[0]
	for i in range(len(rotQuaternions)):
		# print accXYZ[:,i], "\n", np.array([accXYZ[:,i]]).T,"\n",rotQuaternions[i]
		accXYZ[:,i] = np.array(
			    rotQuaternions[i].dot(np.array(accXYZ[:,i]).T)
			).T
		accXYZ[:,i][2] += 0.06
		# print "Res:", accXYZ[:,i]

	# print "!!!RES:",accXYZ[0].tolist()
	# print accXYZ


	"""Without filters"""
	coord_wo = []
	speed_wo = []
	for i in range(len(accXYZ)):
		coord_wo.append(calcCoord(accXYZ[i],accT))

	"""Moving Average"""
	acc_ma = []
	count = 100
	for i in range(len(accXYZ)):
		acc_ma.append(movingAverage(accXYZ[i],count))
	coord_ma = []
	for i in range(len(acc_ma)):
		coord_ma.append(calcCoord(acc_ma[i],accT))
	
	"""Moving Average diffirent windows on Ox data"""
	acc_ma_x = []
	
	acc_ma_x.append(movingAverage(accXYZ[0],10))
	acc_ma_x.append(movingAverage(accXYZ[0],50))
	acc_ma_x.append(movingAverage(accXYZ[0],100))

	coord_ma_x = []
	for i in range(len(acc_ma_x)):
		coord_ma_x.append(calcCoord(acc_ma_x[i],accT))

	"""Exponential Moving Average"""
	acc_ema = []
	count = 100
	for i in range(len(accXYZ)):
		acc_ema.append(movingExpAverage(accXYZ[i],count))

	coord_ema = []
	for i in range(len(acc_ema)):
		coord_ema.append(calcCoord(acc_ema[i],accT))

	"""Exponential Moving Average diffirent windows on Ox data"""
	acc_ema_x = []
	# for i in range(len(accXYZ)):
	acc_ema_x.append(movingExpAverage(accXYZ[0],10))
	acc_ema_x.append(movingExpAverage(accXYZ[0],50))
	acc_ema_x.append(movingExpAverage(accXYZ[0],100))

	"""Kalman acceleration filtering"""
	# print accXYZ[0]
	coord_Kalm = []
	speed_Kalm = []
	p_Kalm = []
	# qprint accT
	for i in range(len(accXYZ)):
		res = calc_kalman(accXYZ[i], accT)
		coord_Kalm.append(res[0])
		speed_Kalm.append(res[1])
		# p_Kalm.append(res[2])

	"""Kalman woe"""
	coord_Kalm_woe = []
	for i in range(len(accXYZ)):
		res = kwoe.calc_kalman(accXYZ[i], accT)
		coord_Kalm_woe.append(res[0])

	"""Kalman woe vs Exponential Moving Average """
	coord_Kalm_woe_ema = []
	count = 100
	for i in range(len(coord_Kalm)):
		coord_Kalm_woe_ema.append(movingExpAverage(movingExpAverage(coord_Kalm_woe[i],count), count))

	"""Kalman vs Moving Average"""
	coord_Kalm_ma = []
	count = 100
	for i in range(len(coord_Kalm)):
		coord_Kalm_ma.append(movingAverage(movingAverage(coord_Kalm[i],count), count))

	"""Kalman vs Exponential Moving Average"""
	coord_Kalm_ema = []
	count = 100
	for i in range(len(coord_Kalm)):
		coord_Kalm_ema.append(movingExpAverage(movingExpAverage(coord_Kalm[i],count), count))

	"""Fiction real (Kalman vs Moving Average vs Moving Average)"""
	coord_Kalm_ma_ma = []
	count = 100
	for i in range(len(coord_Kalm_ma)):
		coord_Kalm_ma_ma.append(movingAverage(coord_Kalm_ma[i], count))

	# plt.figure(6)
	# # real = []
	# for i in range(len(coord_Kalm)):
	# 	plt.plot(coord_Kalm[i], color[i])
	# real = movingAverage(movingAverage(coord_Kalm[1],100),100)
	# 	# real = calcCoord(accXYZ[i],accT)
	# # for i in range(len(coord_Kalm)):
	# plt.plot(real, color[0])
	# plt.plot(coord_Kalm[1], color[2])


	color = 'rgby'

	fig = plt.figure(1)
	ax = fig.gca(projection='3d')
	ax.plot(coord_Kalm[0], coord_Kalm[1], coord_Kalm[2], color="b")
	# ax.plot(coord_Kalm_ma[0], coord_Kalm_ma[1], coord_Kalm_ma[2], color="r")
	# ax.plot(coord_Kalm_ma_ma[0], coord_Kalm_ma_ma[1], coord_Kalm_ma_ma[2], color="g")
	ax.plot(coord_Kalm_ema[0], coord_Kalm_ema[1], coord_Kalm_ema[2], color="r")
	ax.plot([coord_Kalm[0][-1]], [coord_Kalm[1][-1]], [coord_Kalm[2][-1]], 'ro')
	# ax.plot(coord_Kalm[0][::50], coord_Kalm[1][::50], coord_Kalm[2][::50], color="b")
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	# ax.set_xlim3d(0, 20)
	# ax.set_ylim3d(0, 20)
	# plt.show()

	fig = plt.figure(2)
	ax = fig.gca(projection='3d')
	ax.plot(coord_Kalm_woe[0], coord_Kalm_woe[1], coord_Kalm_woe[2], color="b")
	# ax.plot(coord_Kalm_ma[0], coord_Kalm_ma[1], coord_Kalm_ma[2], color="r")
	# ax.plot(coord_Kalm_ma_ma[0], coord_Kalm_ma_ma[1], coord_Kalm_ma_ma[2], color="g")
	ax.plot(coord_Kalm_woe_ema[0], coord_Kalm_woe_ema[1], coord_Kalm_woe_ema[2], color="r")
	ax.plot([coord_Kalm_woe[0][-1]], [coord_Kalm_woe[1][-1]], [coord_Kalm_woe[2][-1]], 'ro')
	# ax.set_xlim(-2, 2)
	# ax.plot(coord_Kalm[0][::50], coord_Kalm[1][::50], coord_Kalm[2][::50], color="b")
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')


	# ax.plot(coord_Kalm_ma[0], coord_Kalm_ma[1], coord_Kalm_ma[2], color="r")

	# plt.figure(5)
	# real = []
	# for i in range(len(coord_Kalm)):
	# plt.plot(p_Kalm[1], color[0])


	plt.figure(6)
	# real = []
	# for i in range(len(coord_Kalm)):
	plt.plot(coord_Kalm[1], color[0])
	plt.plot(coord_Kalm_ma[1], color[2])

	# plt.figure(7)
	# for i in range(len(speed_Kalm)):
	# 	plt.plot(speed_Kalm[i], color[i])


	# plt.show()

	"""Without filters"""

	plt.figure(8)
	plt.title('Without filters')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance, meters')
	for i in range(len(coord_wo)):
		plt.plot(coord_wo[i], color[i])

	# ax.plot(coord_wo[0], coord_wo[1], coord_wo[2], color="g")

	# plt.show()
	"""Example to check if movingAverage works correct
		count = 3 
		# exampleArr = [1,0,1,2,-1,2,0,1,5,10,5,1,2,-2,0,-1,2,3,6,9,12,9,6,3,2,1,0,-1,-1,0,0,1,2,1,1,1,2]
		exampleArr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
		# array = movingAverage(exampleArr,count)
		array = movingExpAverage(exampleArr,count)
		# arrayNew = []
		# for i in range(len(array)):
			# arrayNew.append([float(accT[count-1+i]),float(array[i])])
		# print tabulate(array,headers=['Ax'],floatfmt=".16f")
		"""

	"""Moving Average"""

	plt.figure(9)
	plt.title('Moving average filter')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance, meters')
	for i in range(len(coord_ma)-1):
		plt.plot(coord_ma[i], color[i])

	# ax.plot(coord_ma[0], coord_ma[1], coord_ma[2], color="r")


	plt.figure(10)
	plt.title('Exponentially weighted moving average filter')
	plt.xlabel('Count, unit')
	plt.ylabel('Acceleration Ox, m/s^2')
	plt.plot(accXYZ[0], 'k', lw=0.5)
	for i in range(len(acc_ma_x)):
		plt.plot(acc_ema_x[i], color[i])
	# plt.plot(acc_ema_x[0][400:600], color[0])
	# plt.plot(acc_ma_x[0][400:600], color[2])


	plt.figure(11)
	# plt.title('Moving average vs real data')
	# plt.xlabel('Count, unit')
	# plt.ylabel('Acceleration Ox, m/s^2')
	plt.plot(accXYZ[0], 'k', lw=0.5)
	for i in range(len(acc_ma_x)):
		plt.plot(acc_ma_x[i], color[i])


	plt.figure(12)
	plt.plot(accXYZ[0][::2], 'k', lw=0.5)
	plt.plot(acc_ema_x[2][::2], color[0])
	plt.plot(acc_ma_x[2][::2], color[2])
	print("EMA vs MA")
	print(acc_ema_x[2][0], ":", acc_ma_x[2][0], " diff ", acc_ema_x[2][0] -  acc_ma_x[2][0])
	print(acc_ema_x[2][-1], ":", acc_ma_x[2][-1], " diff ",  acc_ma_x[2][-1] -  acc_ema_x[2][-1])
	
	plt.figure(13)
	plt.title('Moving average for Ox coord with different windows')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance Ox, m')
	for i in range(len(coord_ma_x)):
		plt.plot(coord_ma_x[i], color[i])

	coord_ema_x = []
	for i in range(len(acc_ema_x)):
		coord_ema_x.append(calcCoord(acc_ema_x[i],accT))

	plt.figure(14)
	plt.title('Exponentially moving average for Ox coord with different windows')
	plt.xlabel('Count, unit')
	plt.ylabel('Distance Ox, m')
	for i in range(len(coord_ema_x)):
		plt.plot(coord_ema_x[i], color[i])

	fig = plt.figure(15)
	ax1 = fig.gca(projection='3d')
	# ax1.plot(coord_ema[0][:1000], coord_ema[1][:1000], coord_ema[2][:1000], color="b")
	ax1.plot(coord_wo[0], coord_wo[1], coord_wo[2], color="g")
	ax1.plot(coord_Kalm[0], coord_Kalm[1], coord_Kalm[2], color="b")
	ax1.set_xlabel('X')
	ax1.set_ylabel('Y')
	ax1.set_zlabel('Z')


	plt.show()



