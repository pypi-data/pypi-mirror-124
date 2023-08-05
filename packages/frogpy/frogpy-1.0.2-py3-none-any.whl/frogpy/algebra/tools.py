"""
该文件主要用于实现一些迭代算法，如雅克比　高斯－赛德尔　龙格库塔等迭代算法，
目的是为了迭代求解线性方程组，因为矩阵求逆时间复杂度过于太高．
"""

import numpy as np


def jacobi(a, x, b, times, tol):
    """
    一个迭代算法，目的是求解线性方程组Ax = b的形式，迭代求解x的近似解
    :param a: 一个矩阵
    :param x: 向量，维度与a一致
    :param b: 向量，维度与x一致
    :param times: 一个整数，用于限制迭代的次数，
    :param tol: 一个很小的浮点数，当迭代的向量值x与
    真解之间的误差向量对应的范数小于tol时，终止循环．
    :return: x,list_times, list_err_norm
    """
    size = len(b)
    x1 = np.zeros(size)
    list_times = []  # 用于记录迭代了多少次并返回，方便主函数实现画图
    list_err_norm = []  # 用于记录每次迭代后的范数误差，方便画图
    for i in range(times):  # 控制迭代次数
        for j in range(size):
            x1[j] = b[j]
            for k in range(size):
                if k == j:
                    d = a[j][j]
                else:
                    x1[j] = x1[j] - a[j][k]*x[k]
            x1[j] = x1[j]/d
        for j in range(size):
            x[j] = x1[j]  # 完成一次更新替换
        err = b - a@x
        err_norm = np.linalg.norm(err)
        list_times.append(i)
        list_err_norm.append(err_norm)
        # print(err_norm)
        if err_norm < tol:
            break
    return x, list_times, list_err_norm, err


def csrjacobi(data, indices, indptr,  x, b, times, tol):
    """
    采用压缩矩阵法求解矩阵与向量的乘法，这样当程序运算量较大时候可以节省很多时间
    :param data: 存储矩阵的非零元素
    :param indices: 存储data中元素对应在矩阵的列数
    :param indptr: 存储矩阵中一行的元素在data中的起始位置
    :param x: 需要迭代求解的向量
    :param b: 一个向量
    :param times:迭代的次数
    :param tol: 迭代的精度，采用的是向量的 2-norm　进行计算的
    :return: x　求解的结果, list_times　迭代的次数,
    list_err_norm　迭代的范数误差, err 真解与数值解的误差向量
    """
    size = len(x)
    x1 = np.zeros(size)
    list_times = []  # 用于记录迭代了多少次并返回，方便主函数实现画图
    list_err_norm = []  # 用于记录每次迭代后的范数误差，方便画图
    for i in range(times):  # 控制迭代次数
        for j in range(size):
            x1[j] = b[j]
            for k in range(indptr[j],indptr[j+1]):
                if indices[k] == j:
                    d = data[k]
                else:
                    x1[j] = x1[j] - data[k]*x[indices[k]]
            x1[j] = x1[j] / d
        for j in range(size):
            x[j] = x1[j]  # 完成一次更新替换
        err = np.zeros(size)
        for k in range(size):
            for j in range(indptr[k],indptr[k+1]):
                err[k] += data[j]*x[indices[j]]
            err[k] = b[k] - err[k]
        err_norm = np.linalg.norm(err)  # 2-norm
        list_times.append(i)
        list_err_norm.append(err_norm)
        # print(err_norm)
        if err_norm < tol:
            break
    return x, list_times, list_err_norm, err



def csrAx(data, indices, indptr, x):
    """
    实现矩阵左乘向量的行压缩矩阵乘法
    :param data:
    :param indices:
    :param indptr:
    :param x:
    :return:
    """
    size = len(x)
    b = np.zeros(size)
    for k in range(size):
        for j in range(indptr[k], indptr[k + 1]):
            b[k] += data[j] * x[indices[j]]
    return b


def abs_max_mat(a):
    """
    求矩阵的绝对值最大值
    :param a: 矩阵
    :return: 返回矩阵绝对值最大值
    """
    nr = a.shape[0]
    nc = a.shape[1]
    e = abs(a[0][0])
    for i in range(nr):
        for j in range(nc-1):
            if e < abs(a[i][j+1]):
                e = abs(a[i][j+1])
    return e




