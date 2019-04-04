# coding:utf8
import cv2
import numpy as np
from skimage import io as sio
from skimage.segmentation import felzenszwalb
import matplotlib.pyplot as plt
from _felzenszwalb_cy import _felzenszwalb_cython


def felzenszwalb_test(img,sigma,kernel,k, min_size):
    # 先使用纹理特征滤波，再计算距离
    img = np.asanyarray(img, dtype=np.float) / 255

    # rescale scale to behave like in reference implementation
    k = float(k) / 255.
    img = cv2.GaussianBlur(img, (kernel, kernel), sigma)
    height, width = img.shape[:2]
    num = height * width
    edges = np.zeros(((height - 1) * width * 2 + height * (width - 1) * 2, 3))

    # 使用RGB距离，计算四邻域
    index = np.array([i for i in range(height * width)])
    index = index.reshape((height, width))
    to_left = np.sqrt(((img[:, 1:] - img[:, :-1]) ** 2).sum(axis=2))
    to_right = to_left
    to_up = np.sqrt(((img[1:] - img[:-1]) ** 2).sum(axis=2))
    to_down = to_up


    last, cur = 0, 0
    last, cur = cur, cur + (width - 1) * height
    edges[last: cur, 0] = index[:, 1:].reshape(-1)
    edges[last: cur, 1] = index[:, :-1].reshape(-1)
    edges[last: cur, 2] = to_left.reshape(-1)

    last, cur = cur, cur + (width - 1) * height
    edges[last: cur, 0] = index[:, :-1].reshape(-1)
    edges[last: cur, 1] = index[:, 1:].reshape(-1)
    edges[last: cur, 2] = to_right.reshape(-1)

    last, cur = cur, cur + (height - 1) * width
    edges[last: cur, 0] = index[1:].reshape(-1)
    edges[last: cur, 1] = index[:-1].reshape(-1)
    edges[last: cur, 2] = to_up.reshape(-1)

    last, cur = cur, cur + (height - 1) * width
    edges[last: cur, 0] = index[:-1].reshape(-1)
    edges[last: cur, 1] = index[1:].reshape(-1)
    edges[last: cur, 2] = to_down.reshape(-1)

    # 将边按照不相似度从小到大排序
    edges = [edges[i] for i in range(edges.shape[0])]
    edges.sort(key=lambda x: x[2])

    # 构建无向图（树）
    class universe(object):
        def __init__(self, n, k):
            self.f = np.array([i for i in range(n)])  # 树
            self.r = np.zeros_like(self.f)   # root
            self.s = np.ones((n))  # 存储像素点的个数
            self.t = np.ones((n)) * k  # 存储不相似度
            self.k = k

        def find(self, x):    # Find root of node x
            if x == self.f[x]:
                return x
            return self.find(self.f[x])

        def join(self, a, b):  # Join two trees containing nodes n and m
            if self.r[a] > self.r[b]:
                self.f[b] = a
                self.s[a] += self.s[b]
            else:
                self.f[a] = b
                self.s[b] += self.s[a]
                if self.r[a] == self.r[b]:
                    self.r[b] += 1

    u = universe(num, k)
    for edge in edges:
        a, b = u.find(int(edge[0])), u.find(int(edge[1]))
        if ((a != b) and (edge[2] <= min(u.t[a], u.t[b]))):
            # 更新类标号：将的类a,b标号统一为的标号a。更新该类的不相似度阈值为：k / (u.s[a]+u.s[b])
            u.join(a, b)
            a = u.find(a)
            u.t[a] = edge[2] + k / u.s[a]

    for edge in edges:
        a, b = u.find(int(edge[0])), u.find(int(edge[1]))
        if ((a != b) and ((u.s[a] < min_size) or u.s[b] < min_size)):
            # 分割后会有很多小区域，当区域像素点的个数小于min_size时，选择与其差异最小的区域合并
            u.join(a, b)

    dst = np.zeros_like(img)

    def locate(index):
        return index // width, index % width

    avg_color = np.zeros((num, 3))

    for i in range(num):
        f = u.find(i)
        x, y = locate(i)
        avg_color[f, :] += img[x, y, :] / u.s[f]

    for i in range(height):
        for j in range(width):
            f = u.find(i * width + j)
            dst[i, j, :] = avg_color[f, :]
    return dst


if __name__ == '__main__':
    sigma = 0.5
    kernel = 3
    K, min_size = 500, 50
    image = sio.imread("img/bone.jpg")
    # skimage自带的felzenszwalb算法
    seg1 = felzenszwalb(image, scale=K, sigma=sigma, min_size=min_size)
    # skimage自带的felzenszwalb算法cython版转Python代码,更改了高斯模糊
    seg2 = _felzenszwalb_cython(image, scale=K, sigma=sigma, kernel=kernel,min_size=min_size)
    # felzenszwalb算法的实现，相比于上一种，区别主要在四邻域和颜色还原
    seg3=felzenszwalb_test(image, sigma, kernel,K, min_size)

    fig = plt.figure()
    a = fig.add_subplot(221)
    plt.imshow(image)
    a.set_title("image")

    a = fig.add_subplot(222)
    plt.imshow(seg1)
    a.set_title("seg1")

    a = fig.add_subplot(223)
    plt.imshow(seg2)
    a.set_title("seg2")

    a = fig.add_subplot(224)
    plt.imshow(seg3)
    a.set_title("seg3")
    plt.show()