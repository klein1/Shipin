# -*- coding: utf-8 -*-
import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import numpy as np

def main():
    # 加载图片数据
    # img = skimage.data.astronaut()
    img = skimage.io.imread('img/girl.jpg')

    '''
    执行selective search，regions格式如下
    [
                {
                    'rect': (left, top, width, height),
                    'labels': [...],
                    'size': component_size
                },
                ...
    ]
    '''
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=500, sigma=0.9, min_size=10)

    # 计算一共分割了多少个原始候选区域
    temp = set()
    for i in range(img_lbl.shape[0]):
        for j in range(img_lbl.shape[1]):
            temp.add(img_lbl[i, j, 3])
    print(len(temp))  # 286

    # 计算利用Selective Search算法得到了多少个候选区域
    print(len(regions))  # 570
    # 创建一个集合 元素不会重复，每一个元素都是一个list(左上角x，左上角y,宽,高)，表示一个候选区域的边框
    candidates = set()
    for r in regions:
        # 排除重复的候选区
        if r['rect'] in candidates:
            continue
        # 排除小于 2000 pixels的候选区域(并不是bounding box中的区域大小)
        if r['size'] < 2000:
            continue
        # 排除扭曲的候选区域边框  即只保留近似正方形的
        # x, y, w, h = r['rect']
        # if w / h > 1.2 or h / w > 1.2:
        #     continue
        candidates.add(r['rect'])

    # 在原始图像上绘制候选区域边框
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in candidates:
        print(x, y, w, h)
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    plt.show()

def test():



    pass

if __name__ == "__main__":
    # test()
    main()