# -*- coding: utf-8 -*-
"""
data - усредняемые данные
w    - размер окна
"""
def moving_average(data, w):
	length = len(data)
	if (w > length):
		raise Exception("Окно должно быть меньше количества замеров")
	aver = []
	for i in range(length - w + 1):
		aver.append(reduce(lambda x, y: x + y, data[i:i+w]) / w)
	for i in range(length - w + 1, length):
		prev = aver[-1]
		prev_w = aver[-w]
		k = length - i
		aver.append(prev-(prev_w+data[i])/w)
	return aver

"""
data - усредняемые данные
w    - размер окна
"""
def moving_exp_average(data, w):
	length = len(data)
	if (w > length):
		raise Exception("Окно должно быть меньше количества замеров")
	aver = [data[0]]
	alpha = float(2)/(w+1)
	for i in range(1,length):
		aver.append(data[i]*alpha + (1-alpha)*aver[-1])
	return aver

"""
acc  - ускорение
time - время
w    - размер окна
"""
def calc_coord_ma(acc, time, w):
	acc_ma = []
	for i in range(len(acc)):
		acc_ma.append(moving_average(acc,w))
	res = [0]
	v = x = 0
	print len(acc_ma), len(time)
	for i in range(len(acc_ma)-1):
		t = time[i]
		if i == 0:
			print acc_ma[i+1], time[i+1], t
		v = v + acc_ma[i+1]*(time[i+1]-t)
		x = x + v*(time[i+1]-t) + acc_ma[i+1]*pow(time[i+1]-t, 2)/2
		res.append(x)
	return res

"""
acc  - ускорение
time - время
w    - размер окна
"""
def calc_coord_ema(acc, time, w):
	acc_ema = []
	for i in range(len(acc)):
		acc_ema.append(moving_average(acc,w))
	res = [0]
	v = x = 0
	for i in range(len(acc_ema)-1):
		t = time[i]
		v = v + acc_ema[i+1]*(time[i+1]-t)
		x = x + v*(time[i+1]-t) + acc_ema[i+1]*pow(time[i+1]-t, 2)/2

		res.append(x)
	return res

"""
acc  - ускорение
time - время
"""
def calc_coord(acc, time):
	res = [0]
	v = x = 0
	for i in range(len(acc)-1):
		t = time[i]
		v = v + acc[i+1]*(time[i+1]-t)
		x = x + v*(time[i+1]-t) + acc[i+1]*pow(time[i+1]-t, 2)/2

		res.append(x)
	return res
