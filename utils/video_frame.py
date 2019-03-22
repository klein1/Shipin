import cv2, shutil

def loop():
    vc = cv2.VideoCapture('../static/video/wsl.mp4')  # 读入视频文件
    c = 1

    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False

    timeF = 1000  # 视频帧计数间隔频率

    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if (c % timeF == 0):  # 每隔timeF帧进行存储操作
            cv2.imwrite('images/' + str(c) + '.jpg', frame)  # 存储为图像
        c = c + 1
        cv2.waitKey(1)
    vc.release()

def capture(video,output):
    vc = cv2.VideoCapture(video)
    c = 0
    timeF = 1000
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
        shutil.copy("static/img/pure.jpg",output)

    timeF = 1000

    while rval:
        rval, frame = vc.read()
        if (c % timeF == 0):
            cv2.imwrite(output, frame)
            if c > 0:
                break
        c = c + 1
        cv2.waitKey(1)

    vc.release()

if __name__ == "__main__":
    capture('../static/video/20190322142011.mp4','output.jpg')