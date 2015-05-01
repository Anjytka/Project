# -*- coding: utf-8 -*-
"""
data - усредняемые данные
m    - размер окна
"""
def movingAverage(data, m):
	if (m > data):
		raise Exception("Interval have to be less then data length")
	aver = []
	for i in range(len(data) - m + 1):
		aver.append(reduce(lambda x, y: x + y, data[i:i+m]) / m)
	# for i in range(len(data)-1):
	# 	aver.append(data[i])
		# yield aver
	return aver