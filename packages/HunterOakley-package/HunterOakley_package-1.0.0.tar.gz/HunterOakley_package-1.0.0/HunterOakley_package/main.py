# coding=utf-8


import itertools

list1 = (1, 2, 3, 4)
list2 = (500, 600, 800, 900)


def get_combinator():
    """
    获取组合数，笛卡尔积
    :return: none
    """
    for i in itertools.product(list1, list2):
        print(i)


def print_multiplication(n):
    """
    打印乘法表
    :param n:打印多少的乘法表
    :return: none
    """
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print("%d*%d=%d" % (j, i, (j * i)), end=" ")
        print()


def add(a, b):
    """
    两数相加
    :param a: num
    :param b:num
    :return:
    """
    print(a + b)


def series(n):
    """
    斐波那契数列
    1 1 2 3 5 8 13...
    :param n:数列第几项 n >0 int
    :return:数列第几项对应的数
    """
    if n == 1 or n == 2:
        return 1
    else:
        return series(n - 2) + series(n - 1)


if __name__ == '__main__':
    # print_multiplication(9)
    # add(1, 2)
    print(series(8))
