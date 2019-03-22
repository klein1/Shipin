import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('img/bone.jpg.',0)

fast=cv2.FastFeatureDetector_create()#获取FAST角点探测器
kp=fast.detect(img,None)#描述符
img = cv2.drawKeypoints(img,kp,img,color=(255,255,0))#画到img上面
print ("Threshold: ", fast.getThreshold())#输出阈值
print ("nonmaxSuppression: ", fast.getNonmaxSuppression())#是否使用非极大值抑制
print ("Total Keypoints with nonmaxSuppression: ", len(kp))#特征点个数

height,width = img.shape[:2]  #获取原图像的水平方向尺寸和垂直方向尺寸。
img = cv2.resize(img,(int(1/2*width),int(1/2*height)),interpolation=cv2.INTER_CUBIC)
cv2.imshow('fast',img)
cv2.waitKey(0)