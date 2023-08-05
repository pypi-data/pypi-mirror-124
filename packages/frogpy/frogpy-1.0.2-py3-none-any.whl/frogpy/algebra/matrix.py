import numpy as np


def Maindiagonal(n, r):
    """

    :param n: 矩阵的维度
    :param r: 对角线元素
    :return: 一个对角矩阵
    """
    a = np.zeros((n, n))
    for i in range(n):
        a[i][i] = r
    return a


# r1:main r2:上负对角线元素　r3:下负对角线元素
def tri_diagonal(n, r1, r2, r3):
    """

    :param n: 矩阵的维度
    :param r1: 主对角元素
    :param r2: 次上对角元素
    :param r3: 次下对角元素
    :return: 对称正定的矩阵(或者说是三对角矩阵)
    """
    a = np.zeros((n, n))
    for i in range(n):
        if i == 0:
            a[i][i] = r1
            a[i][i + 1] = r2
        elif i == n - 1:
            a[i][i] = r1
            a[i][i - 1] = r3
        else:
            a[i][i] = r1
            a[i][i + 1] = r2
            a[i][i - 1] = r3
    return a


def M_tri_diagonal(nx, ny, b1, b2, b3):
    """

    :param nx:
    :param ny:
    :param b1:正对角块矩阵
    :param b2: 次上对角块矩阵
    :param b3: 次下对角块矩阵
    :return: 一个五带的对称正定矩阵
    """
    N = nx * ny
    a = np.zeros((N, N))
    for i in range(nx):
        if i == 0:
            a[0:ny, 0:ny] = b1
            a[0:ny, ny:2 * ny] = b2
        elif i == nx - 1:
            a[N - ny:N, N - ny:N] = b1
            a[N - ny:N, N - 2 * ny:N - ny] = b3
        else:
            a[i * ny:(i + 1) * ny, i * ny:(i + 1) * ny] = b1
            a[i * ny:(i + 1) * ny, (i + 1) * ny:(i + 2) * ny] = b2
            a[i * ny:(i + 1) * ny, (i - 1) * ny:i * ny] = b3
    return a


def five_diagonal(nx, ny, r1, r2, r3, r4, r5):
    """
    返回一个具有五带非零元素的对称正定矩阵
    :param nx: x轴的节点数（看情况可以是内节点和外界点数）
    :param ny: y轴的节点数
    :param r1: 主对角
    :param r2: 上次对角
    :param r3: 下次对角
    :param r4: 上次角的右边非零元素
    :param r5: 下次对角左边非零元素
    :return: 一个五带的对称正定矩阵
    """
    d = tri_diagonal(ny, r1, r2, r3)  # 主对角块矩阵
    b = Maindiagonal(ny, r4)  # 上对角块矩阵
    c = Maindiagonal(ny, r5)  # 下对角块矩阵
    a = M_tri_diagonal(nx, ny, d, b, c)
    return a


def csrmatrix(A, data, indices, indptr):
    k = 0
    nr = A.shape[0]
    nc = A.shape[1]
    for i in range(nr):
        for j in range(nc):
            if A[i][j] != 0:
                data[k] = A[i][j]
                indices.append(j)
                k += 1
        indptr.append(k)


# 写一些测试内容，在次判断下导入该包的文件不会输出这些内容
# 也可以单独写一个函数来写测试内容，然后在这里调用它,比如def main():
if __name__ == "__main__":
    print("test")
    # main()
