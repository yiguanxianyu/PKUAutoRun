# -*- coding:utf-8 -*
"""
感谢：
@yuchenxi2000 https://github.com/yuchenxi2000 
https://github.com/PKUNoRun/PKUNoRun/issues/17
https://gist.github.com/yuchenxi2000/adaf2b29e584ae715c160c98229235d6

主要改动是提高了程序运行的效率，并去除了无用的部分
"""

from math import radians, sin, cos, sqrt, pi
from random import random

import numpy as np
import numpy.random as npr
import scipy.interpolate
import scipy.optimize
from scipy.stats import norm

center = np.array([116.30713526140399,
                   39.986307321096085])  # 操场中心点（调了很久！本人没有精确定位工具！）
alpha = radians(4.5)  # 操场偏离正北4.5度（调出来的）
r = 36.5  # 半径
d_curve = r * pi  # 半圆长度
d_straight = 200 - d_curve  # 直线部分长度
w = 1.22  # 跑道宽度
earth_radians = radians(6371393)


class ST:
    """
    我们假设跑步过程中由于避让其他跑步者等会换道。
    这个类计算跑到t距离时的偏移量（在第几道）
    先随机取一系列离散的点，然后插值得到连续的函数
    """

    def __init__(self, start, end):
        # n 指的是每 n 米换一次跑道？
        n = 200
        num = int(end - start) // n + 1
        # xp和yp是待插值的点
        xp = np.linspace(start - 20, end + 20, num)

        offset = npr.randn(num)
        offset = np.where(offset > 1.25, 2 * offset, offset)
        offset = np.where(offset < -1, -1, offset)
        yp = (offset * 2 + 5) * w

        yp[0] = random() * 2 + 6
        yp[-1] = random() * 2 + 3

        self.f = scipy.interpolate.interp1d(xp, yp, kind='cubic')


s_t_func = None


def rot(angle):
    """
    逆时针旋转矩阵
    """
    sin_a = sin(angle)
    cos_a = cos(angle)
    return np.array([[cos_a, -sin_a], [sin_a, cos_a]])


def d_latlon(p1, p2):
    """
    计算两点间的距离。原文件使用了较复杂的算法，代价较高
    这里使用较为相对简单的算法代替，精度不会损失很多
    """
    lon_diff, lat_diff = p1 - p2
    lon_diff *= cos((p1[1] + p2[1]) * 0.00872664625997165)
    return sqrt(lat_diff * lat_diff + lon_diff * lon_diff) * earth_radians


def p_d_v(p, d, v):
    """
    距离P点v方向上、距离d的点
    """
    if d < 0:
        d, v = -d, -v

    cos_lat2 = cos(p[1] * 0.0174532925199433) ** 2
    d_lat2, d_lon2 = v * v

    def foo(t):
        return sqrt(d_lon2 + d_lat2 * cos_lat2) * t * earth_radians - d

    x = scipy.optimize.bisect(foo, 0, 0.001)

    return p + x * v


rotate_alpha = rot(alpha)
# 下面关键点由中心点经过平移、旋转得到
# 操场北部圆心点
Pu = p_d_v(center, d_straight / 2, rotate_alpha @ np.array([0.0, 1.0]))
# 操场南部圆心点
Pd = p_d_v(center, d_straight / 2, rotate_alpha @ np.array([0.0, -1.0]))

# 四个矩形顶点，从左上开始逆时针
P0 = p_d_v(Pu, r, rotate_alpha @ np.array([-1, 0]))
P1 = p_d_v(Pd, r, rotate_alpha @ np.array([-1, 0]))
P2 = p_d_v(Pd, r, rotate_alpha @ np.array([1, 0]))
P3 = p_d_v(Pu, r, rotate_alpha @ np.array([1, 0]))

# 一系列向量
P0_to_P1 = P1 - P0  # P0指向P1的向量，其余类推
P2_to_P3 = P3 - P2
Pu_to_P0 = P0 - Pu
Pu_to_P3 = P3 - Pu
Pd_to_P1 = P1 - Pd
Pd_to_P2 = P2 - Pd
# 归一化
P0_to_P1 /= np.linalg.norm(P0_to_P1)
P2_to_P3 /= np.linalg.norm(P2_to_P3)
Pu_to_P0 /= np.linalg.norm(Pu_to_P0)
Pu_to_P3 /= np.linalg.norm(Pu_to_P3)
Pd_to_P1 /= np.linalg.norm(Pd_to_P1)
Pd_to_P2 /= np.linalg.norm(Pd_to_P2)

d1 = d_straight
d2 = d1 + d_curve
d3 = d2 + d_straight


def move(t, s):
    """
    改变跑道
    t: 离出发点距离
    s: 跑道偏移量（一道为0，二道为一个跑道宽度，以此类推）
    """
    t = t % 400.0

    if t <= d1:  # 第一直道
        # 分为两步，forward是获取下一个位置的点，第二次调用计算跑道的偏移
        forward = p_d_v(P0, t, P0_to_P1)
        return p_d_v(forward, s, Pu_to_P0)

    elif t <= d2:  # 第一弯道
        beta = (t - d_straight) / r
        return p_d_v(Pd, r + s, rot(beta) @ Pd_to_P1)

    elif t <= d3:  # 第二直道
        forward = p_d_v(P2, t - d_straight - d_curve, P2_to_P3)
        return p_d_v(forward, s, Pd_to_P2)

    else:  # 第二弯道
        beta = (t - d_straight - d_straight - d_curve) / r
        return p_d_v(Pu, r + s, rot(beta) @ Pu_to_P3)


def pts(t):
    t = t % 400.0

    if t <= d1:  # 第一直道
        return p_d_v(P0, t, P0_to_P1)
    elif t <= d2:  # 第一弯道
        beta = (t - d_straight) / r
        return p_d_v(Pd, r, rot(beta) @ Pd_to_P1)
    elif t <= d3:  # 第二直道
        return p_d_v(P2, t - d_straight - d_curve, P2_to_P3)
    else:  # 第二弯道
        beta = (t - d_straight - d_straight - d_curve) / r
        return p_d_v(Pu, r, rot(beta) @ Pu_to_P3)


def adjust_pp_d(t0: float, d0: float):
    """
    根据取定的两点，用二分法精确求解下一个路径点
    t0: 目前已经走到的位置, 即起点
    d: 前进的距离, 即终点
    s_t: 确定换道
    """

    def f(t):
        return d_latlon(pts(t), pts(t0)) - d0

    t2 = t0 + d0
    while d_latlon(pts(t0), pts(t2)) < d0:
        t2 = t2 + t2 - t0

    return scipy.optimize.bisect(f, t0, t2)


def get_smooth_random_shift(num_points):
    """
    生成「平滑」的随机偏移量
    每次迭代，基于前一个点上下浮动，浮动方向以正态分布偏向于中间
    """
    val = []
    last = 0
    sign = 0
    prob = 2 / 3
    rands = npr.rand(num_points)
    rands_prob = rands / prob
    
    for i in range(num_points):
        if rands[i] > prob:
            # 三分之一可能性不改方向
            sign = 0
        elif rands_prob[i] > norm.cdf(last, scale=5):
            # 更多
            sign = 1
        else:
            # 更少
            sign = -1
        
        last += sign
        val.append(last)   
        
    return np.array(val) * 0.00001


def gen_record(distance, speed):
    """
    生成点轨迹
    """
    npr.seed(int(random() * 1e5))
    # 起始点位置，默认为操场西北角位置附近
    start_point = 50 * (random() + 1)

    global s_t_func
    s_t_func = ST(start_point, start_point + distance).f

    points = []
    dist_generated = 0.0
    t = start_point
    step = 4  # 基本步长
    num_points = 10000 # 生成轨迹点的数量

    rand_offset = npr.randn(num_points) * 0.02
    dist_straight = rand_offset + step
    dist_curve = rand_offset + step * 0.867

    rand_shift = get_smooth_random_shift(num_points).reshape(2, -1).T
    rand_shift[:, 1] *= cos(radians(center[1]))

    i = 0
    while dist_generated < distance:
        temp = t % 400
        if temp < d1 or d2 < temp < d3:
            d0 = dist_straight[i]
        else:
            d0 = dist_curve[i]  # 前进的距离

        t1 = adjust_pp_d(t, d0)
        s1 = s_t_func(t)
        # 给轨迹加上随机漂移
        point = move(t1, s1) + rand_shift[i]

        if points:
            dist_generated += d_latlon(point, points[-1])

        points.append(point)

        i += 1
        t = t1

    time = []
    cumulate_time = 0
    rs = (npr.randn(len(points)) / 10 + 1) * 1000 / speed
    for i in range(len(points)):
        if i == 0:
            dur_time = 0
        elif i == len(points) - 1:
            dist = d_latlon(points[i - 1], points[i])
            dur_time = dist / rs[i]
        else:
            dist = d_latlon(points[i + 1], points[i - 1])
            dur_time = 0.5 * dist / rs[i]

        cumulate_time += dur_time
        time.append(cumulate_time)

    p = np.array(points)[:, [1, 0]]
    index = np.array(time).reshape(-1, 1)
    return np.append(p, index, axis=1)
