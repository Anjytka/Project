# -*- coding: utf-8 -*-

from math import *
from random import *
import matplotlib.pyplot as plt
import numpy as np

H = np.matrix([[1., 0.]]) # матрица измерений, связывающая истинный вектор состояния и вектор произведенных измерений
R = np.matrix([[1.]]) # ковариационная матрица шума наблюдений
I = np.identity(2) # единичная матрица
sigma_a = 1.

def _kalman(acc, dt_mass, x, P, F, G):
    global R, H, I, sigma_a
    result = []
    speed = []
    for n in range(len(dt_mass)):
        # Предсказание 
        F = np.matrix([[1., dt_mass[n]], [0, 1.]]) # функция пересчета состояния
        G = np.matrix([[pow(dt_mass[n],2)/2], [dt_mass[n]]]) # функция пересчета состояния
        Q = G*G.T*pow(sigma_a,2)
        x = F * x + G*acc[n]
        P = F * P * F.T + Q
        
        # Корректировка
        z = np.matrix([[acc[n]]])
        y = z - H * x # Отклонение полученного на шаге k наблюдения от наблюдения, ожидаемого при произведенной экстраполяции 
        R = np.matrix([[10.]])
        S = H * P * H.T + R # Ковариационная матрица вектора отклонения
        K = P * H.T * np.linalg.inv(S) # Оптимальная по Калману матрица коэффициентов усиления
        x = x + (K * y) # Коррекция ранее полученной экстраполяции вектора состояния
        P = (I - K * H) * P # Расчет ковариационной матрицы оценки вектора состояния системы
        result.append(x.item(0,0))
        speed.append(x.item(1,0))

    return [result, speed, p]

def calc_kalman(acc, time):
    dt_mass = [time[i]-time[i-1] for i in range(1, len(time))]
    (x, P, F, G) = reset(dt_mass[0])   
    X = kalman(acc, dt_mass, x, P, F, G)
    print X[0][-1], ":", X[1][-1]
    return X

def _reset(dt):
    x = np.matrix([[0.], [0.]]) # координата и скорость
    P = np.matrix([[100., 0.], [0., 100.]]) # L=1000 => опирается на апостериорную информацию
    F = np.matrix([[1., dt], [0., 1.]]) # функция пересчета состояния
    G = np.matrix([[pow(dt,2)/2], [dt]]) # функция пересчета состояния
    
    return (x, P, F, G)
















