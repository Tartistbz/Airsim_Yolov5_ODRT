import cv2
import torch
import torch.hub
import time

CLASSES = ("drone", "car", "person", "bird", "cat", "dog")

# Model
model_path = r'D:\yolov5-master\Airsim connect\my_best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)


def draw(image, boxes, scores, classes):
    for box, score, cl in zip(boxes, scores, classes):
        left, top, right, bottom = box
        left = int(left)
        top = int(top)
        right = int(right)
        bottom = int(bottom)
        cl = int(cl)

        # 修改框的颜色为红色 (0, 0, 255)
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

        # 定义标签文本
        label = '{0} {1:.2f}'.format(CLASSES[cl], score)
        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

        # 添加红色底色的标签
        cv2.rectangle(image, (left, top - label_size[1] - base_line),
                      (left + label_size[0], top), (0, 0, 255), cv2.FILLED)
        # 将文字颜色修改为白色
        cv2.putText(image, label, (left, top - base_line),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, lineType=cv2.LINE_AA)


def yolo_recognition(img):
    """
    yolo 识别物体
    :param img:
    :return boxes, classes, scores: boxes格式为[[left, top, right, bottom], ...]
    """
    results = model(img)
    # xmin, ymin, xmax, ymax, confidence, class
    rec_result = results.xyxy[0]
    rec_result_np = rec_result.cpu().numpy()
    boxes = rec_result_np[:, 0:4]
    score = rec_result_np[:, 4]
    classes = rec_result_np[:, 5]
    return boxes, classes, score


if __name__ == "__main__":
    # videos
    video_path = "sample_720p.mp4"
    cap = cv2.VideoCapture(video_path)

    frames, loopTime = 0, time.time()
    while cap.isOpened():
        frames += 1
        ret, img = cap.read()

        # Inference
        boxes, classes, scores = yolo_recognition(img)

        if boxes is not None:
            draw(img, boxes, scores, classes)
        # show output
        cv2.imshow("post process result", img)
        # Press Q on keyboard to exit
        key = cv2.waitKey(1)  # 等待按键命令, 1000ms 后自动关闭
    # Closes all the frames
    cap.release()
    cv2.destroyAllWindows()
