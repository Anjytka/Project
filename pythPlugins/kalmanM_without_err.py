# -*- coding: utf-8 -*-

from math import *
from random import *
import matplotlib.pyplot as plt
import numpy as np

class matrix:

    # implements basic operations of a matrix class

    def __init__(self, value):
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0

    def zero(self, dimx, dimy):
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]

    def identity(self, dim):
        # check if valid dimension
        if dim < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dim
            self.dimy = dim
            self.value = [[0 for row in range(dim)] for col in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1

    def show(self):
        for i in range(self.dimx):
            print self.value[i]
        print ' '

    def __add__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to add"
        else:
            # add if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res

    def __sub__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to subtract"
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res

    def __mul__(self, other):
        # check if correct dimensions
        if self.dimy != other.dimx:
            raise ValueError, "Matrices must be m*n and n*p to multiply"
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
            return res

    def transpose(self):
        # compute transpose
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res

    # Thanks to Ernesto P. Adorio for use of Cholesky and CholeskyInverse functions

    def Cholesky(self, ztol = 1.0e-5):
        # Computes the upper triangular Cholesky factorization of
        # a positive definite matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)

        for i in range(self.dimx):
            S = sum([(res.value[k][i]) ** 2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError, "Matrix not positive-definite"
                res.value[i][i] = sqrt(d)
            for j in range(i + 1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0.0
                res.value[i][j] = (self.value[i][j] - S) / res.value[i][i]
        return res

    def CholeskyInverse(self):
        # Computes inverse of matrix given its Cholesky upper Triangular
        # decomposition of matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)

        # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k] * res.value[j][k] for k in range(j + 1, self.dimx)])
            res.value[j][j] = 1.0 / tjj ** 2 - S / tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k] * res.value[k][j] for k in range(i + 1, self.dimx)]) / self.value[i][i]
        return res

    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res

    def __repr__(self):
        return repr(self.value)

##########################################################

H = matrix([[1., 0.]]) # матрица измерений, связывающая истинный вектор состояния и вектор произведенных измерений
R = matrix([[4.]]) # ковариационная матрица шума наблюдений
I = matrix([[1., 0.], [0., 1.]]) # единичная матрица

def kalman(acc, dt_mass, x, P, F, G):
    # global acc, speed, result, u, F, H, R, I
    global R
    result = []
    speed = []
    for n in range(len(dt_mass)):

        # measurement update
        z = matrix([[acc[n]]])
        y = z - H * x # Отклонение полученного на шаге k наблюдения от наблюдения, ожидаемого при произведенной экстраполяции 
        S = H * P * H.transpose() + R # Ковариационная матрица вектора отклонения
        K = P * H.transpose() * S.inverse() # Оптимальная по Калману матрица коэффициентов усиления
        x = x + (K * y) # Коррекция ранее полученной экстраполяции вектора состояния
        P = (I - K * H) * P # Расчет ковариационной матрицы оценки вектора состояния системы

        # prediction 
        # G.show()
        # x.show()
        x = F * x + matrix([[G.value[0][0]*acc[n]], [G.value[1][0]*acc[n]]])
        P = F * P * F.transpose()
        F = matrix([[1., dt_mass[n]], [0, 1.]]) # функция пересчета состояния
        G = matrix([[pow(dt_mass[n],2)/2], [dt_mass[n]]]) # функция пересчета состояния
        # r = y*y.transpose()
        # R = r
        # R.show()
        # R = matrix([[4.0]])
        result.append(x.value[0][0])
        speed.append(x.value[1][0])
    return [result, speed]

def calc_kalman(acc, time):
    # global acc, speed, result, x, P

    dt_mass = [time[i]-time[i-1] for i in range(1, len(time))]
    # print dt_mass
    (x, P, F, G) = reset(dt_mass[0])   
    X = kalman(acc, dt_mass, x, P, F, G)

    # if (iter > 0):
    #     plt.figure(iter)
    #     plt.plot(acc, 'r')
    #     plt.plot(X[0], 'g')
    #     plt.plot(X[1], 'y')

    print X[0][-1], ":", X[1][-1]

    return X

def reset(dt):
    # global speed, result, x, P, u, F, H, R, I
    x = matrix([[0.], [0.]]) # координата и скорость
    P = matrix([[5000., 0.], [0., 5000.]]) # L=1000 => опирается на апостериорную информацию
    # u = matrix([[0.], [0.]]) # 
    F = matrix([[1., dt], [0., 1.]]) # функция пересчета состояния
    G = matrix([[pow(dt,2)/2], [dt]]) # функция пересчета состояния
    
    return (x, P, F, G)
















