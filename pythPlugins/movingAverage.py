# -*- coding: utf-8 -*-
"""
data - усредняемые данные
m    - размер окна
"""
def movingAverage(data, m):
	length = len(data)
	if (m > length):
		raise Exception("Interval have to be less then data length")
	aver = []
	for i in range(length - m + 1):
		aver.append(reduce(lambda x, y: x + y, data[i:i+m]) / m)
	for i in range(length - m + 1, length):
		prev = aver[-1]
		prev_w = aver[-m]
		k = length - i
		# aver.append(reduce(lambda x, y: x + y, data[i:i+k]) / k)
		aver.append(prev-(prev_w+data[i])/m)
		# print i+1, " : ", aver[-1]
	# for i in range(len(data)-1):
	# 	aver.append(data[i])
		# yield aver
	return aver


def movingExpAverage(data, m):
	length = len(data)
	if (m > length):
		raise Exception("Interval have to be less then data length")
	aver = [data[0]]
	alpha = float(2)/(m+1)
	for i in range(1,length):
		aver.append(data[i]*alpha + (1-alpha)*aver[-1])
	return aver


def calcCoord(acc, time):
	res = [0]
	v = x = 0
	for i in range(len(acc)-1):
		t = time[i]
		v = v + acc[i+1]*(time[i+1]-t)
		x = x + v*(time[i+1]-t) + acc[i+1]*pow(time[i+1]-t, 2)/2

		res.append(x)
	return res