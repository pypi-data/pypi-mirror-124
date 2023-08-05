'''
封套扭曲实现
本次1.0版本初步实现5中arch效果
'''

import os
# os.chdir("..")
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from deepsvg.svglib.geom import Point
from deepsvg.svglib.svg import SVG
from deepsvg.svglib.svg_path import SVGPath
from deepsvg.svglib.utils import to_gif

from deepsvg.difflib.tensor import SVGTensor
from deepsvg.difflib.utils import *
from deepsvg.difflib.loss import *
from deepsvg.svglib.geom import Bbox,Point


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import torch
from xml.dom import expatbuilder

#读取svg里的path
def from_str(svg_str: str):
    svg_path_groups = []

    SVG_list=[]
    svg_dom = expatbuilder.parseString(svg_str, False)
    svg_root = svg_dom.getElementsByTagName('svg')[0]

    viewbox_list = list(map(float, svg_root.getAttribute("viewBox").split(" ")))
    view_box = Bbox(*viewbox_list)

    primitives = {
        "path": SVGPath
    }

    for tag, Primitive in primitives.items():
        for x in svg_dom.getElementsByTagName(tag):
            svg_path_groups.append(Primitive.from_xml(x))
            SVG_list.append(SVG([Primitive.from_xml(x)], view_box))
        return SVG(svg_path_groups, view_box),SVG_list

#读取轮廓点边界框属性
def find_bbox(points):
    return[points[:,0].min(),points[:,0].max(),points[:,1].min(),points[:,1].max(), (points[:,0].min()+points[:,0].max())/2,
          (points[:,1].min()+points[:,1].max())/2,
           points[:,0].max()- points[:,0].min(),
          points[:,1].max()- points[:,1].min()]

#读取svg并取轮廓点，只对单张svg操作
def get_points_color_insvg(svg_path,p_n=10):
    with open(svg_path, "r") as f:
        svg_str = f.read()

    svg,svg_list = from_str(svg_str)
    svg_path_fillcolor = []
    svg_path_indx = []
    svg_path_tensor = []
    for svg_sp in svg_list:
        #每一个path单独处理
        svg_sp = svg_sp.to_path().simplify_arcs()
        svg_path_fillcolor.append(list([svg_sp.svg_path_groups[i].fill for i in range(len(svg_sp.svg_path_groups))]))
        svg_path_indx.append(list(np.where(svg_sp.to_tensor()[:, 0] == 0)[0])+\
                                  [svg_sp.to_tensor().shape[0]])
        svg_path_tensor.append(svg_sp.to_tensor())
        # plot_points(SVGTensor.from_data(svg_sp.to_tensor()).sample_points(n=5), show_color=True)
        # plt.show()
    bh_indx = svg_path_indx
    # print(bh_indx)
    bh_color = svg_path_fillcolor
    svg_tensor = torch.cat(svg_path_tensor,axis=0)
    # print('svg_tensor shape',svg_tensor.shape)
    svg_target = SVGTensor.from_data(svg_tensor)
    p_target = svg_target.sample_points(n=p_n)
    # print('p_target shape:',p_target.shape)

    bbox = find_bbox(p_target)
    return p_target, bh_indx, bh_color, bbox


def trans_points(cont, bbox, n=10, arch_per=0.3, pos=True, fix='top', mode='arch'):
    if mode == 'arch_right':
        cont = torch.flip(cont, [1])
        pos = False
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

    if mode=='arch' or mode=='arch_right':
        # xiahu neg
        if pos:
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
    elif mode=='single_arch':
        if fix == 'top':
            if not pos:
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h
                circle_c = [center_x, c[1] + r * np.cos(arch_a)]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc = circle_c[0] + r * np.sin(a_cont)
                y_arc = circle_c[1] - r * np.abs(np.cos(a_cont))

                y_rate = (cont[:, 1] - a[1]) / h
                new_x = y_rate * cont[:, 0] + (1 - y_rate) * x_arc
                new_y = (y_rate) * a[1] + (1 - y_rate) * y_arc

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
        else:
            if pos:
                r = (w / 2) / np.sin(arch_a)  # +0.15#+0.7
                upper_r = r + h  # *(w/h)
                circle_c = [center_x, a[1] + r * np.cos(arch_a)]  # c[0]
                a_cont = ((cont[:, 0] - center_x) / (w / 2)) * arch_a  # left - ,right +  (不均匀)
                x_arc = circle_c[0] + r * np.sin(a_cont)
                y_arc = circle_c[1] - r * np.abs(np.cos(a_cont))

                y_rate = (c[1] - cont[:, 1]) / h
                new_x = y_rate * (x_arc - cont[:, 0]) + cont[:, 0]
                new_y = y_rate * (y_arc - c[1]) + c[1]

    transed_points2 = np.array([new_x, new_y])

    if mode == 'arch_right':
        transed_points2 = np.flip(transed_points2, 0)
        w2 = max(transed_points2[0, :]) - min(transed_points2[0, :])
        cx, cy = (max(transed_points2[0, :]) + min(transed_points2[0, :])) / 2, (
                    max(transed_points2[1, :]) + min(transed_points2[1, :])) / 2
        transed_points2[0, :] = (transed_points2[0, :] - cx) * float((bbox[3] - bbox[2])) / w2 + float(
            bbox[3] + bbox[2]) / 2
        transed_points2[1, :] = (transed_points2[1, :] - cy) * float((bbox[3] - bbox[2])) / w2 + float(
            bbox[1] + bbox[0]) / 2
    else:
        w2 = max(transed_points2[0, :]) - min(transed_points2[0, :])
        cx, cy = (max(transed_points2[0, :]) + min(transed_points2[0, :])) / 2, (
                    max(transed_points2[1, :]) + min(transed_points2[1, :])) / 2
        transed_points2[0, :] = (transed_points2[0, :] - cx) * float((bbox[1] - bbox[0])) / w2 + float(
            bbox[1] + bbox[0]) / 2
        transed_points2[1, :] = (transed_points2[1, :] - cy) * float(bbox[1] - bbox[0]) / w2 + float(
            bbox[3] + bbox[2]) / 2
    transed_points2 = np.around(transed_points2,decimals=3)
    # plt.scatter(transed_points2[0,:],transed_points2[1,:])
    return transed_points2

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

def save_l_svg(transed_points,indx_zi,color_zi, file_path=None,n=10):
    pred_bbox = find_bbox(transed_points.T)
    with_viewbox = str(float(pred_bbox[0]))+' '+str(float(pred_bbox[2]))+' '+str(float(pred_bbox[1]))+' '+str(float(pred_bbox[3]))
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
        p_str = ''
        print('indx_xiao',indx_xiao)
        p_zi_nums = (indx_xiao[-1]-(len(indx_xiao)-1)*2)*(n-1)
        szi_points = transed_points[:,:p_zi_nums]
        transed_points = transed_points[:,p_zi_nums:]
        color = color_zi[j]
        last_inx = 0
        if len(indx_xiao)>2:
            for i in range(len(indx_xiao) - 2):#path里的笔画
                sinx = indx_xiao[i]
                einx = indx_xiao[i + 1]
                p_num = (einx - sinx - 2) * (n-1)
                print(sinx, einx, p_num,szi_points.shape)
                p_pred = szi_points[:,last_inx:last_inx+p_num]
                p_str += gen_svgstr(p_pred)

                last_inx = last_inx + p_num

                if i == len(indx_xiao) - 3:
                    p_pred = szi_points[:,last_inx:]
                    p_str += gen_svgstr(p_pred)
        else:
            p_pred = szi_points[:,:]
            p_str += gen_svgstr(p_pred)

        if color[0]=="":
            color='black'
        path_svg = '<path d="{}" fill="{}"/>'.format(p_str, color)
        # print(path_svg)
        svg = svg + str((f'{path_svg}'))

    svg = svg + str(('</svg>'))
    # print(svg)
    if file_path is not None:
        with open(file_path, 'w') as f:
            f.write(svg)
    return svg

def main(svgpath,sample_n=10,arch_per=0.2,pos=True,fix='top', mode='arch',file_path = r'C:\Users\25790\Downloads\res.svg'):
    read_points, bh_indx, bh_color, points_bbox = get_points_color_insvg(svgpath, p_n=sample_n)
    transed_points = trans_points(read_points, points_bbox, n=sample_n, arch_per=arch_per, pos=pos, fix=fix, mode=mode)
    svg = save_l_svg(transed_points, bh_indx, bh_color, file_path=file_path)


if __name__ == "__main__":
    main(r"C:\Users\25790\Downloads\封套_业务需求\Artboard 27.svg")




