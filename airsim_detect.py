import time

import airsim
import numpy as np
import yolo_orin_api
import cv2

client = airsim.MultirotorClient(ip="192.168.123.102")

camera_name = '0'  # 前向中间	0,底部中间 3
image_type = airsim.ImageType.Scene  # 彩色图airsim.ImageType.Scene, Infrared
while 1:
    response = client.simGetImage(camera_name, image_type, vehicle_name='')  # simGetImage接口的调用方式如下
    if response:
        # 转换成opencv图片格式
        img_bgr = cv2.imdecode(np.array(bytearray(response), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读
        # boxes格式为[[left, top, right, bottom], ...]
        boxes, classes, scores = yolo_orin_api.yolo_recognition(img_bgr)
        if boxes is not None:
            yolo_orin_api.draw(img_bgr, boxes, scores, classes)
            index = 0
            for cat in classes:
                cat_name = yolo_orin_api.CLASSES[cat.astype(int)]
                print(cat_name)

        # show output
        cv2.imshow("preview", img_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("-------------------")
    time.sleep(0.1)