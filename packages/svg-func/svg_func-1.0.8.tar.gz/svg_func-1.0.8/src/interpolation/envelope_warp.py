'''
封套扭曲实现
本次1.0版本初步实现5中arch效果
'''

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import os
# os.chdir("..")
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import time
# st1 = time.time()
from interpolation.deepsvg.svglib.svg import SVG
from interpolation.deepsvg.svglib.svg_path import SVGPath
from interpolation.deepsvg.difflib.tensor import SVGTensor
from interpolation.deepsvg.difflib.utils import *
from interpolation.deepsvg.difflib.loss import *
from interpolation.deepsvg.svglib.geom import Bbox,Point

# print('import time:',time.time()-st1)

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import torch
from xml.dom.minidom import parse, parseString
import copy
import urllib

# print('import time:',time.time()-st1)

#读取svg里的path
def from_str(svg_str: str):
    svg_path_groups = []
    SVG_list=[]

    domTree = parseString(svg_str)
    rootNode = domTree.documentElement

    primitives = {
        "path": SVGPath
    }

    for tag, Primitive in primitives.items():
        for x in rootNode.getElementsByTagName(tag):
            svg_path_groups.append(Primitive.from_xml(x))
            SVG_list.append(SVG([Primitive.from_xml(x)]))
        return SVG(svg_path_groups),SVG_list,domTree

#读取轮廓点边界框属性
def find_bbox(points):
    return[points[:,0].min(),points[:,0].max(),points[:,1].min(),points[:,1].max(), (points[:,0].min()+points[:,0].max())/2,
          (points[:,1].min()+points[:,1].max())/2,
           points[:,0].max()- points[:,0].min(),
          points[:,1].max()- points[:,1].min()]

#读取svg并取轮廓点，只对单张svg操作
def get_points_color_insvg(svg_path,p_n=10):
    try:
        with urllib.request.urlopen(svg_path) as conn:
            svg_str = conn.read()
    except:
        with open(svg_path, 'r') as file:
            svg_str = file.read()
        # svg_str = svg_path

    _, svg_list, domTree = from_str(svg_str)
    svg_path_fillcolor = []
    svg_path_indx = []
    svg_path_hz = []
    svg_path_tensor = []

    for svg_sp in svg_list:
        # 每一个path单独处理
        svg_sp = svg_sp.to_path().simplify_arcs()
        svg_path_fillcolor.append(list([svg_sp.svg_path_groups[i].fill for i in range(len(svg_sp.svg_path_groups))]))
        s_indx = list(np.where(svg_sp.to_tensor()[:, 0] == 0)[0]) + \
                 [svg_sp.to_tensor().shape[0]]
        s_hz = []
        # 是否是M开头Z结尾
        if len(s_indx) >= 3:
            for in0 in s_indx[1:-1]:
                if svg_sp.to_tensor()[:, 0][in0 - 1] == 6:
                    s_hz.append(1)
                else:
                    s_hz.append(0)
        if svg_sp.to_tensor()[:, 0][-1] == 6:
            s_hz.append(1)
        else:
            s_hz.append(0)
        svg_path_indx.append(s_indx)
        svg_path_hz.append(s_hz)
        svg_path_tensor.append(svg_sp.to_tensor())
        # print(svg_sp.to_tensor()[:, 0])

    bh_indx = svg_path_indx
    # print(bh_indx, svg_path_fillcolor)
    bh_color = svg_path_fillcolor

    svg_tensor = torch.cat(svg_path_tensor, axis=0)
    # print('svg_tensor shape', svg_tensor.shape)
    svg_target = SVGTensor.from_data(svg_tensor)
    p_target = svg_target.sample_points(n=p_n)
    word_bbox = find_bbox(p_target)

    return p_target, bh_indx, bh_color, svg_path_hz, word_bbox, domTree


def trans_points(cont, bbox, n=10, arch_per=0.3, pos=True, fix='top', mode='arch'):
    or_bbox = copy.deepcopy(bbox)
    if pos == 'right' or pos == 'left':
        cont = torch.flip(cont, [1])
        bbox = find_bbox(cont)
    if pos == 'left':
        cont[:, 1] *= (-1)
        bbox = find_bbox(cont)

    cont = np.array(cont)
    bbox = np.array(bbox)
    a = [bbox[0], bbox[2]]
    b = [bbox[1], bbox[2]]
    c = [bbox[0], bbox[3]]
    d = [bbox[1], bbox[3]]
    # 角度百分比（与90度比），圆心左右对称有
    arch_a = math.pi / 2 * arch_per
    center_x = (a[0] + b[0]) / 2
    w = (b[0] - a[0])
    h = c[1] - a[1]
    print(bbox)

    if mode == 'arch':
        # xiahu neg
        if pos == 'up':
            r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
            upper_r = r + h
            circle_c = [center_x, c[1] + r * np.cos(arch_a)]
            # print('r', circle_c, r, arch_a)
            # print((cont[0, 0] - center_x) / (w / 2))
            a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
            r_cont = r + (upper_r - r) * (c[1] - cont[:, 1]) / h  # +
            new_x = circle_c[0] + r_cont * np.sin(a_cont)
            new_y = circle_c[1] - r_cont * np.cos(a_cont)
        #             plt.scatter(new_x, new_y)
        # print(bbox, arch_a)
        else:
            r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
            upper_r = r + h  # *(w/h)
            circle_c = [center_x, a[1] - r * np.cos(arch_a)]
            # print('r', circle_c, r, arch_a)
            a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
            # print((cont[0, 0] - center_x) / (w / 2))
            r_cont = r + (upper_r - r) * (cont[:, 1] - a[1]) / h  # +
            new_x = circle_c[0] + r_cont * np.sin(a_cont)
            new_y = circle_c[1] + r_cont * np.cos(a_cont)
            # plt.scatter(new_x, new_y)
            # print(bbox, arch_a)
    elif mode == 'single_arch':
        if pos == 'up':
            r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
            upper_r = r + h  # *(w/h)
            circle_c = [center_x, a[1] + r * np.cos(arch_a)]  # c[0]
            a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
            x_arc = circle_c[0] + r * np.sin(a_cont)
            y_arc = circle_c[1] - r * np.abs(np.cos(a_cont))

            y_rate = (c[1] - cont[:, 1]) / h
            new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
            new_y = y_rate * (y_arc - c[1]) + c[1]
        else:
            r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
            upper_r = r + h  # *(w/h)
            circle_c = [center_x, c[1] - r * np.cos(arch_a)]  # c[0]
            a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
            x_arc = circle_c[0] + r * np.sin(a_cont)
            y_arc = circle_c[1] + r * np.abs(np.cos(a_cont))

            y_rate = (cont[:, 1] - a[1]) / h
            new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
            new_y = y_rate * (y_arc - a[1]) + a[1]

    transed_points2 = np.array([new_x, new_y])

    if pos == 'right' or pos == 'left':
        if pos == 'left':
            transed_points2[1, :] *= (-1)
        transed_points2 = np.flip(transed_points2, 0)

        w2 = max(transed_points2[0, :]) - min(transed_points2[0, :])
        print(float((bbox[1] - bbox[0])), float((bbox[3] - bbox[2])), w2, float((or_bbox[3] - or_bbox[2])) / w2)
        cx, cy = (max(transed_points2[0, :]) + min(transed_points2[0, :])) / 2, (
                max(transed_points2[1, :]) + min(transed_points2[1, :])) / 2
        transed_points2[0, :] = (transed_points2[0, :] - cx) * float((bbox[3] - bbox[2])) / w2 + float(
            or_bbox[1] + or_bbox[0]) / 2
        transed_points2[1, :] = (transed_points2[1, :] - cy) * float((bbox[3] - bbox[2])) / w2 + float(
            or_bbox[1] + or_bbox[0]) / 2

    else:
        w2 = max(transed_points2[0, :]) - min(transed_points2[0, :])
        cx, cy = (max(transed_points2[0, :]) + min(transed_points2[0, :])) / 2, (
                max(transed_points2[1, :]) + min(transed_points2[1, :])) / 2
        transed_points2[0, :] = (transed_points2[0, :] - cx) * float((bbox[1] - bbox[0])) / w2 + float(
            bbox[1] + bbox[0]) / 2
        transed_points2[1, :] = (transed_points2[1, :] - cy) * float(bbox[1] - bbox[0]) / w2 + float(
            bbox[3] + bbox[2]) / 2
    transed_points2 = np.around(transed_points2, decimals=3)
    # plt.scatter(transed_points2[0,:],transed_points2[1,:])
    return transed_points2


def trans_points_random4poly(p_target, c_svg, word_bbox, n=10, mode='polygon'):
    if mode == 'poly_circle':
        word_bbox = np.array(word_bbox)
        width = word_bbox[6]
        height = word_bbox[7]
        n = 10
        iw = width / n
        ih = height / n
        print(iw, ih)
        left = list([word_bbox[0], word_bbox[3] - ih * i] for i in range(n))
        bottom = list([word_bbox[0] + iw * i, word_bbox[2]] for i in range(n))
        right = list([word_bbox[1], word_bbox[2] + ih * i] for i in range(n))
        top = list([word_bbox[1] - iw * i, word_bbox[3]] for i in range(n))
        control_points = np.array([left, bottom, right, top]).reshape(-1, 2)
        control_points[:, 0] = (control_points[:, 0] - control_points[:, 0].mean()) * 1.01 + control_points[:, 0].mean()
        control_points[:, 1] = (control_points[:, 1] - control_points[:, 1].mean()) * 1.01 + control_points[:, 1].mean()
        print(control_points.shape)

        # new_control_points
        r = max(width, height) / 2 * 0.9
        ia = math.pi / (2 * n)
        r_left_a = list([math.pi * (7 / 4) - ia * i for i in range(n)])
        r_left = np.array([r * np.sin(r_left_a), r * np.cos(r_left_a)]).T
        print(r_left.shape)
        r_bottom_a = list([math.pi * (5 / 4) - ia * i for i in range(n)])
        r_bottom = np.array([r * np.sin(r_bottom_a), r * np.cos(r_bottom_a)]).T

        r_right_a = list([math.pi * (3 / 4) - ia * i for i in range(n)])
        r_right = np.array([r * np.sin(r_right_a), r * np.cos(r_right_a)]).T

        r_top_a = list([math.pi * (9 / 4) - ia * i for i in range(n)])
        r_top = np.array([r * np.sin(r_top_a), r * np.cos(r_top_a)]).T

        new_control_points = np.array([r_left, r_bottom, r_right, r_top]).reshape(-1, 2)
    else:
        c_svg = np.array(c_svg)
        print(c_svg)

        # 平移缩放无所谓：
        print(word_bbox)
        word_bbox = np.array(word_bbox)
        control_points = np.array([[word_bbox[0], word_bbox[3]],
                                   [word_bbox[0], word_bbox[2]],
                                   [word_bbox[1], word_bbox[2]],
                                   [word_bbox[1], word_bbox[3]]])
        new_control_points = np.array(c_svg)
        control_points[:, 0] = (control_points[:, 0] - control_points[:, 0].mean()) * 1.01 + control_points[:, 0].mean()
        control_points[:, 1] = (control_points[:, 1] - control_points[:, 1].mean()) * 1.01 + control_points[:, 1].mean()
        print(control_points)

    p_target = np.array(p_target)
    print(p_target.shape)
    v0 = copy.deepcopy(p_target)
    v0 = v0[:, np.newaxis, :].repeat([control_points.shape[0]], axis=1)  # 8437,4,2
    print('V0.shape', v0.shape)

    vi = copy.deepcopy(control_points)
    vi = vi[np.newaxis, :, :].repeat([v0.shape[0]], axis=0)
    vj = np.concatenate((control_points[1:], [control_points[0]]), axis=0)
    vj = vj[np.newaxis, :, :].repeat([v0.shape[0]], axis=0)
    r0i = np.sqrt(((v0 - vi) ** 2).sum(axis=2))
    r0j = np.sqrt(((v0 - vj) ** 2).sum(axis=2))
    rij = np.sqrt(((vj - vi) ** 2).sum(axis=2))
    dn = 2 * r0i * r0j
    r = (r0i ** 2 + r0j ** 2 - rij ** 2) / dn
    print('r shape', r.shape)
    r[r > 1] = 1
    r[r < -1] = -1
    A = np.arccos(r)

    _r = np.sqrt(((v0 - vi) ** 2).sum(axis=2))
    A_i = np.concatenate((A[:, -1][:, np.newaxis], A[:, 0:-1]), axis=1)
    print(A.shape, A_i.shape, _r.shape)
    W = (np.tan(A_i / 2) + np.tan(A / 2)) / _r

    W = np.array(W)
    Ws = W.sum(axis=1)
    L = W / Ws[:, np.newaxis].repeat([W.shape[1]], axis=1)
    print('L.shape', L.shape)

    new_control_points = new_control_points[np.newaxis, :, :].repeat([L.shape[0]], axis=0)
    nx_ny = (L[:, :, np.newaxis].repeat([2], axis=2) * new_control_points).sum(axis=1)
    new_p = nx_ny
    new_p = np.array(new_p)
    # print('new_p shape', new_p.shape)
    # plt.show()
    # print('######################')
    # plt.figure(figsize=(20, 20))
    new_control_points = np.concatenate((new_control_points, [new_control_points[0]]), axis=0)
    # plt.plot(new_control_points[:, 0], -new_control_points[:, 1], c='red')
    # plt.scatter(new_p[:, 0], -new_p[:, 1])
    # print(find_bbox(new_p))
    # print('#############################')
    # plt.show()

    return new_p.T

def trans_points_circle(p_target,svg_bbox):
    p_target = np.array(p_target)
    svg_bbox = np.array(svg_bbox)
    # resize到正方形，原点为中心点
    z_l = max(svg_bbox[1] - svg_bbox[0], svg_bbox[3] - svg_bbox[2])
    center = [(svg_bbox[1] + svg_bbox[0]) / 2, (svg_bbox[3] + svg_bbox[2]) / 2]
    p_target[:, 0] = (p_target[:, 0] - center[0]) / (svg_bbox[1] - svg_bbox[0]) * z_l
    p_target[:, 1] = (p_target[:, 1] - center[1]) / (svg_bbox[3] - svg_bbox[2]) * z_l

    copy_p = copy.deepcopy(p_target)
    # x,y 轴上的点不进入计算
    copy_p[:, 0][p_target[:, 0] == 0] = z_l / 4
    copy_p[:, 1][p_target[:, 0] == 0] = z_l / 4
    copy_p[:, 0][p_target[:, 1] == 0] = z_l / 4
    copy_p[:, 1][p_target[:, 1] == 0] = z_l / 4

    # 矩形四周角点不进入计算
    copy_p[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                    z_l / 2 * np.sin(math.pi / 4)]
    copy_p[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == -z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                     -z_l / 2 * np.sin(math.pi / 4)]
    copy_p[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == -z_l / 2)] = [-z_l / 2 * np.sin(math.pi / 4),
                                                                                      -z_l / 2 * np.sin(math.pi / 4)]
    copy_p[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == z_l / 2)] = [-z_l / 2 * np.sin(math.pi / 4),
                                                                                     z_l / 2 * np.sin(math.pi / 4)]

    # 正方形中心点在原点
    # 正方形四周是圆的边缘，中心轴在原位置不变（圆直径径是边长）。平行y连线和平行x连线是越来越大平缓的圆弧。圆弧的夹角从90度逐渐降为0，
    # 边上的两点是圆弧上的点，于x轴或者y轴的夹角从45度降为0。一个矩形里的点，可以画出y连线于x连线的两段弧，计算弧（2个圆）的交点就是在圆内的点。
    # 因为都基于第一象限计算，只取第一象限的交点作为变换后的点位置。四周角点的点和xy轴上的点不纳入计算，直接取得，计算中会出现极值。
    ###思考
    ###这是将原来的直线连线都变为了圆弧，如果是椭圆，或者其他弧线，应该是同理。最大弧线逐渐降级成为直线，需要找方法。本质上是bazier

    incir_copyp = copy.deepcopy(copy_p)
    row_rc_rate = np.abs(incir_copyp[:, 1]) / (z_l / 2)
    row_cir_arch = row_rc_rate * math.pi / 2
    row_qt_arch = row_rc_rate * math.pi / 4
    row_qt_len = z_l * np.cos(row_qt_arch)
    row_cir_r = (row_qt_len / 2) / (np.sin(row_cir_arch / 2))
    row_cir_ceter = np.zeros((row_cir_r.shape[0], 2))
    row_cir_ceter[:, 1] = -row_cir_r * np.cos(row_cir_arch / 2) + z_l * np.sin(row_qt_arch) / 2
    print(row_cir_ceter.shape)

    col_rc_rate = abs(incir_copyp[:, 0]) / (z_l * 0.5)
    col_cir_arch = col_rc_rate * math.pi / 2
    col_qt_arch = col_rc_rate * math.pi / 4
    col_qt_len = z_l * np.cos(col_qt_arch)
    col_cir_r = (col_qt_len / 2) / (np.sin(col_cir_arch / 2))
    col_cir_ceter = np.zeros((col_cir_r.shape[0], 2))
    col_cir_ceter[:, 0] = -col_cir_r * np.cos(col_cir_arch / 2) + z_l * np.sin(col_qt_arch) / 2

    def insec(p1, r1, p2, r2):
        x = p1[:, 0]
        y = p1[:, 1]
        R = r1
        a = p2[:, 0]
        b = p2[:, 1]
        S = r2
        d = np.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
        #     print(np.sort(d-(R+S)),np.sort(d-(np.abs(R-S))),np.sort(d))
        #     print(np.unique((d-(R+S))>0),(d-(np.abs(R-S))).any() < 0,d.any() == 0)
        if np.sort(d - (R + S))[0] > 0 or (d - (np.abs(R - S))).any() < 0:
            # print("Two circles have no intersection")
            return None, None
        elif d.any() == 0:
            # print("Two circles have same center!")
            return None, None
        else:
            A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
            h = np.sqrt(R ** 2 - A ** 2)
            x2 = x + A * (a - x) / d
            y2 = y + A * (b - y) / d
            x3 = np.around(x2 - h * (b - y) / d, 2)
            y3 = np.around(y2 + h * (a - x) / d, 2)
            x4 = np.around(x2 + h * (b - y) / d, 2)
            y4 = np.around(y2 - h * (a - x) / d, 2)
            c1 = np.array([x3, y3])
            c2 = np.array([x4, y4])
            return c1, c2

    c1, c2 = insec(row_cir_ceter, row_cir_r, col_cir_ceter, col_cir_r)
    print(c1.shape, c2.shape)
    c1 = c1.T
    c2 = c2.T
    ###只要第一象限的点
    incir_copyp[np.logical_and(c1[:, 0] > 0, c1[:, 1] > 0)] = c1[np.logical_and(c1[:, 0] > 0, c1[:, 1] > 0)]
    incir_copyp[np.logical_and(c2[:, 0] > 0, c2[:, 1] > 0)] = c2[np.logical_and(c2[:, 0] > 0, c2[:, 1] > 0)]
    incir_copyp = incir_copyp * copy_p / np.abs(copy_p) #正负号赋值

    incir_copyp[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                         z_l / 2 * np.sin(math.pi / 4)]
    incir_copyp[np.logical_and(p_target[:, 0] == z_l / 2, p_target[:, 0] == -z_l / 2)] = [z_l / 2 * np.sin(math.pi / 4),
                                                                                          -z_l / 2 * np.sin(
                                                                                              math.pi / 4)]
    incir_copyp[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == -z_l / 2)] = [
        -z_l / 2 * np.sin(math.pi / 4), -z_l / 2 * np.sin(math.pi / 4)]
    incir_copyp[np.logical_and(p_target[:, 0] == -z_l / 2, p_target[:, 0] == z_l / 2)] = [
        -z_l / 2 * np.sin(math.pi / 4), z_l / 2 * np.sin(math.pi / 4)]

    incir_copyp[:, 0][p_target[:, 0] == 0] = 0
    incir_copyp[:, 1][p_target[:, 0] == 0] = p_target[:, 1][p_target[:, 0] == 0]
    incir_copyp[:, 0][p_target[:, 1] == 0] = p_target[:, 0][p_target[:, 1] == 0]
    incir_copyp[:, 1][p_target[:, 1] == 0] = 0

    return incir_copyp.T

def write_path_insvg(p_pred,color,svg):
    if not color:
        color='black'
    path_svg = '<path d="{}" fill="{}"/>'.format("M" + str(p_pred[0, 0]) + " " + str(
        p_pred[0, 1]) + " " + " ".join(
        "L" + str(p_pred[0, a]) + " " + str(
            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z", color)

    svg = svg + str((f'{path_svg}'))
    return svg

def gen_svgstr(p_pred):
    p_str = "M" + str(p_pred[0, 0]) + " " + str(
        p_pred[1, 0]) + " " + " ".join(
        "L" + str(p_pred[0, a]) + " " + str(
            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
    return p_str

def save_l_svg(domTree, transed_points,indx_zi,color_zi, hz_zi, file_path=None,n=10):
    names = domTree.documentElement.getElementsByTagName("path")

    transed_points = np.around(transed_points, decimals=3)
    pred_bbox = find_bbox(transed_points.T)
    with_viewbox = str(float(pred_bbox[0])) + ' ' + str(float(pred_bbox[2])) + ' ' + str(
        float(pred_bbox[1])) + ' ' + str(float(pred_bbox[3]))
    # fill_attr = f'fill="black" stroke="black"'
    fill_attr = ''
    marker_attr = ''
    path_filling = '1'
    svg = str((
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{with_viewbox}">'
        f'{""}'))
    print(color_zi)

    for j in range(len(indx_zi)):
        indx_xiao = indx_zi[j]
        hz_xiao = hz_zi[j]
        p_str = ''
        print('indx_xiao', indx_xiao, hz_xiao)

        p_zi_nums = (indx_xiao[-1] - (len(indx_xiao) - 1) - sum(hz_xiao)) * (n - 1)
        szi_points = transed_points[:, :p_zi_nums]
        transed_points = transed_points[:, p_zi_nums:]
        color = color_zi[j]
        last_inx = 0
        if len(indx_xiao) > 2:
            for i in range(len(indx_xiao) - 2):  # path里的笔画
                sinx = indx_xiao[i]
                einx = indx_xiao[i + 1]
                gp = 2
                if hz_xiao[i] == 0:
                    gp = 1

                p_num = (einx - sinx - gp) * (n - 1)
                if p_num <= 0:
                    p_pred = szi_points[:, last_inx:last_inx + 1]
                    p_str += "M" + str(p_pred[0, 0]) + " " + str(
                        p_pred[1, 0])
                else:
                    print(sinx, einx, p_num, last_inx, szi_points.shape)
                    p_pred = szi_points[:, last_inx:last_inx + p_num]
                    p_str += "M" + str(p_pred[0, 0]) + " " + str(
                        p_pred[1, 0]) + " " + " ".join(
                        "L" + str(p_pred[0, a]) + " " + str(
                            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
                    #                 print('###############',"M" + str(p_pred[0, 0]) + " " + str(
                    #                         p_pred[1, 0]) + " " + " ".join(
                    #                         "L" + str(p_pred[0, a]) + " " + str(
                    #                             p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z")
                    #                 print(p_pred)
                    #                     plot_points(p_pred.T, show_color=True)
                    #     #                 plt.plot(p_pred[0,:],p_pred[1,:],c='red')
                    #                     plt.show()

                    last_inx = last_inx + p_num

                if i == len(indx_xiao) - 3:
                    print(last_inx, szi_points.shape)
                    p_pred = szi_points[:, last_inx:]
                    p_str += "M" + str(p_pred[0, 0]) + " " + str(
                        p_pred[1, 0]) + " " + " ".join(
                        "L" + str(p_pred[0, a]) + " " + str(
                            p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
        #                     plot_points(p_pred.T, show_color=True)
        #     #                 plt.plot(p_pred[0,:],p_pred[1,:],c='red')
        #                     plt.show()
        else:
            p_pred = szi_points[:, :]
            p_str += "M" + str(p_pred[0, 0]) + " " + str(
                p_pred[1, 0]) + " " + " ".join(
                "L" + str(p_pred[0, a]) + " " + str(
                    p_pred[1, a]) for a in range(p_pred.shape[1] - 1)) + " Z"
        #             plot_points(p_pred.T, show_color=True)
        # #           plt.plot(p_pred[0,:],p_pred[1,:],c='red')
        #             plt.show()

        print(color)
        if color[0] == "":
            color = ['black']
        path_svg = '<path d="{}" fill="{}"/>'.format(p_str, color[0])
        print(path_svg)
        svg = svg + str((f'{path_svg}'))
        names[j].setAttribute("d", p_str)

    svg = svg + str(('</svg>'))
    # print(svg)
    if file_path is not None:
        with open(file_path, 'w') as f:
            f.write(svg)
        with open(file_path.replace('.svg', '_changes.svg'), 'w') as f:
            # 缩进 - 换行 - 编码
            #             a=domTree.writexml(f, addindent='  ', encoding='utf-8')
            nsvg=''
            # svg = str((
            #     f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{with_viewbox}">'
            #     f'{""}'))
            nsvg += str(domTree.toxml('UTF-8'), encoding="utf-8")
            # svg += str(('</svg>'))
            f.write(nsvg)

    # print(domTree.toxml('UTF-8'))
    return svg, str(domTree.toxml('UTF-8'), encoding="utf-8")

def main(svgpath,sample_n=10,c_svg=None,arch_per=0.2,pos='up',fix='top', mode='arch',file_path = r'C:\Users\25790\Downloads\res.svg'):
    import time
    st=time.time()
    read_points, bh_indx, bh_color,bh_hz, points_bbox,domTree = get_points_color_insvg(svgpath, p_n=sample_n)
    rt = time.time()
    print('read time:',rt-st)
    if 'arch' in mode:
        transed_points = trans_points(read_points, points_bbox, n=sample_n, arch_per=arch_per, pos=pos, fix=fix,
                                      mode=mode)
    elif mode == 'polygon':
        #         c_svg = [[10,30],[0,0],[40,0],[30,30]]
        transed_points = trans_points_random4poly(read_points, c_svg, points_bbox, n=sample_n, mode='polygon')
    elif mode == 'circle':
        transed_points = trans_points_circle(read_points, points_bbox)
    trt = time.time()
    # print('transed time:',trt-rt)
    svg, xml = save_l_svg(domTree,transed_points, bh_indx, bh_color, bh_hz, file_path=file_path)
    sat = time.time()
    # print('saved time:',sat-trt)
    print('total used time:',sat-st)

    return svg, xml


if __name__ == "__main__":

    svg,xml = main(r"C:\Users\25790\Downloads\气.svg",file_path=None)
    # print(time.time()-st1)





