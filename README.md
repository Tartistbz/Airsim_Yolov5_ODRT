# AirSim Drone Detection(EN) 

This repository contains code and models for real-time drone detection and control. Below is a description of each file:

## File Descriptions

### 1. `airsim_detect.py`
Used for real-time drone detection, primarily responsible for window generation. It works with the `yolo_orin_api.py` file for detection and real-time annotation. Only `airsim_detect.py` needs to be started.

### 2. `yolo_orin_api.py`
Works with `airsim_detect.py` for detection and real-time annotation.

### 3. `quard.py`
AirSim control API commands, used to control the drone's state.

### 4. `airsim_test.py` (another real-time detection program)
This is another program for real-time detection, implemented using pygame. It allows controlling the drone via keyboard while detecting.

## Model Descriptions

### 1. `my_best.pt`
A YOLOv5 model, trained by ourselves, used for drone detection.

### 2. `yolov5s.pt`
Official YOLOv5 model.

### 3. `yolov8n.pt`
Official YOLOv8 model.

## Configuration Document

### 1. `readme.pdf`
Chinese configuration document, detailing the setup and usage of the first real-time monitoring program.

## Startup Sequence

1. Start AirSim.
2. Start the detection program `airsim_detect.py`.

## Usage

1. Start AirSim.
2. Run the detection program:
    ```sh
    python airsim_detect.py
    ```

Contributions and feedback are welcome!

GitHub repository URL: [https://github.com/Tartistbz/Airsim_Yolov5_ODRT.git](https://github.com/Tartistbz/Airsim_Yolov5_ODRT.git)


# AirSim Drone Detection (CH)

本仓库包含用于无人机实时检测和控制的代码和模型。以下是各文件的介绍：

## 文件说明

### 1. `airsim_detect.py`
用于实现无人机的实时检测，主要负责生成窗口显示。配合`yolo_orin_api.py`文件进行检测和实时标注。只需启动`airsim_detect.py`即可。

### 2. `yolo_orin_api.py`
与`airsim_detect.py`配合工作，负责检测和实时标注。

### 3. `quard.py`
AirSim控制API指令文件，用于操控无人机状态。

### 4. `airsim_test.py` (另一个实时检测程序)
这是另一个实现实时检测的程序，使用pygame实现。在检测的同时，还可以通过键盘控制无人机。

## 模型说明

### 1. `my_best.pt`
YOLOv5模型，自己训练的，用于无人机检测。

### 2. `yolov5s.pt`
YOLOv5官方模型。

### 3. `yolov8n.pt`
YOLOv8官方模型。

## 配置文档

### 1. `readme.pdf`
中文配置文档，详细介绍了第一种实时监测程序的配置和使用方法。

## 启动顺序

1. 先启动AirSim。
2. 启动检测程序`airsim_detect.py`。

## 使用方法

1. 启动AirSim。
2. 运行检测程序：
    ```sh
    python airsim_detect.py
    ```

欢迎贡献和反馈！


