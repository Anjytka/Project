# -*- coding: utf-8 -*-
import numpy as np

def _calc_angles(acc, gyr, time):
	K = 0.06
	dt_mass = [time[i]-time[i-1] for i in range(1, len(time))]
	gyr_x = 0
	gyr_y = 0
	gyr_z = 0
	result = []
	for i in range(len(acc)):
		acc_x = np.arctan(acc[i][0]/
			np.sqrt(pow(acc[i][1],2)+pow(acc[i][2],2)))
		acc_y = np.arctan(acc[1]/
			np.sqrt(pow(acc[i][0],2)+pow(acc[i][2],2)))
		acc_z = np.arctan(acc[2]/
			np.sqrt(pow(acc[i][0],2)+pow(acc[i][1],2)))
		gyr_x = gyr_x + gyr[i][0]*dt_mass[i]
		gyr_y = gyr_y + gyr[i][1]*dt_mass[i]
		gyr_z = gyr_z + gyr[i][2]*dt_mass[i]
		res_x = (1-K)*gyr_x + K*acc_x
		res_y = (1-K)*gyr_y + K*acc_y
		res_z = (1-K)*gyr_z + K*acc_z
		result.append([res_x, res_y, res_z])
	return result

def _calc_quaternions(angles):
	result = []
	for i in range(len(angles)):
		a = angles[i]
		qr = np.cos(a[0])*np.cos(a[1])*np.cos(a[2]) - np.sin(a[0])*np.sin(a[1])*np.sin(a[2])
		qi = np.cos(a[0])*np.cos(a[1])*np.sin(a[2]) - np.sin(a[0])*np.sin(a[1])*np.cos(a[2])
		qj = np.cos(a[0])*np.sin(a[1])*np.cos(a[2]) - np.sin(a[0])*np.cos(a[1])*np.sin(a[2])
		qk = np.sin(a[0])*np.cos(a[1])*np.cos(a[2]) - np.cos(a[0])*np.sin(a[1])*np.sin(a[2])
		result.append([qr, qi, qj, qk])
	return result

def _get_quar_matrix_from_quat(qtXYZ):
	result = []
	# rotXYZ = np.array(rotXYZ)
	for i in range(len(qtXYZ[0])):
		qmatrix = _get_quaternion_matrix(qtXYZ[:,i])
		result.append(qmatrix[0:3,0:3])
		if i == 0:
			print "QW: ", qtXYZ[:,i]
			# print "QM: ", qmatrix[0:3,0:3]
	return result

def _get_quaternion_matrix(quaternion):
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

def rotateAccels(dataAcc, dataGyr, dataTime):
	angles = _calc_angles(dataAcc, dataGyr, dataTime)
	quaters = np.array(_calc_quaternions(angles))
	qMatrixes = _get_quar_matrix_from_quat(quaters)

	"""Rotate acceleration"""
	for i in range(len(qMatrixes)):
		dataAcc[:,i] = np.array(
			    qMatrixes[i].dot(np.array(dataAcc[:,i]).T)
			).T
	return dataAcc