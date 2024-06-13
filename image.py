import sys
import cv2
import airsim
import pygame
import time
import numpy as np
import os
import shutil
# 初始化 AirSim 客户端
AirSim_client = airsim.MultirotorClient()
AirSim_client.confirmConnection()
AirSim_client.enableApiControl(True)
AirSim_client.armDisarm(True)
AirSim_client.takeoffAsync().join()
# 定义摄像头图像类型
image_types = {
    "scene": airsim.ImageType.Scene,
    "depth": airsim.ImageType.DepthVis,
    "seg": airsim.ImageType.Segmentation,
    "normals": airsim.ImageType.SurfaceNormals,
    "segmentation": airsim.ImageType.Segmentation,
    "disparity": airsim.ImageType.DisparityNormalized
}

# 设定基础速率和基础油门
base_rate = 0.2
base_throttle = 0.55
# 加速倍率和加速标志
speedup_ratio = 4.0
speedup_flag = False
# 改变时间和启用改变标志
change_time = 0.0
enable_change = True
# 控制迭代标志
control_iteration = False

# 初始化 Pygame
pygame.init()
# 创建窗口
screen = pygame.display.set_mode((1024, 768))
# 设置窗口标题
pygame.display.set_caption('keyboard ctrl @FPV')
# 填充窗口背景色
screen.fill((0, 0, 0))

existing_data_cleared = False
data_path = "lidar/data"
shutil.rmtree(data_path)
os.makedirs(data_path, exist_ok=True)
# 主循环
while True:
    pitch_rate = 0.0
    yaw_rate = 0.0
    roll_rate = 0.0
    throttle = base_throttle
    control_iteration = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    scan_wrapper = pygame.key.get_pressed()

    if scan_wrapper[pygame.K_SPACE]:
        scale_ratio = speedup_ratio
    else:
        scale_ratio = speedup_ratio / speedup_ratio

    if time.time() - change_time > 2:
        enable_change = True

    if scan_wrapper[pygame.K_LCTRL] and scan_wrapper[pygame.K_c] and enable_change:
        enable_change = False
        change_time = time.time()

    if scan_wrapper[pygame.K_a] or scan_wrapper[pygame.K_d]:
        control_iteration = True
        yaw_rate = (scan_wrapper[pygame.K_a] - scan_wrapper[pygame.K_d]) * scale_ratio * base_rate

    if scan_wrapper[pygame.K_UP] or scan_wrapper[pygame.K_DOWN]:
        control_iteration = True
        pitch_rate = (scan_wrapper[pygame.K_UP] - scan_wrapper[pygame.K_DOWN]) * scale_ratio * base_rate

    if scan_wrapper[pygame.K_LEFT] or scan_wrapper[pygame.K_RIGHT]:
        control_iteration = True
        roll_rate = -(scan_wrapper[pygame.K_LEFT] - scan_wrapper[pygame.K_RIGHT]) * scale_ratio * base_rate

    if scan_wrapper[pygame.K_w] or scan_wrapper[pygame.K_s]:
        control_iteration = True
        throttle = base_throttle + (scan_wrapper[pygame.K_w] - scan_wrapper[pygame.K_s]) * scale_ratio * base_rate

    if pitch_rate > 1.0:
        pitch_rate = 1.0
    elif pitch_rate < -1.0:
        pitch_rate = -1.0

    if yaw_rate > 1.0:
        yaw_rate = 1.0
    elif yaw_rate < -1.0:
        yaw_rate = -1.0

    if roll_rate > 1.0:
        roll_rate = 1.0
    elif roll_rate < -1.0:
        roll_rate = -1.0

    if throttle > 1.0:
        throttle = 1.0
    elif throttle < 0.0:
        throttle = 0.0

    if control_iteration:
        AirSim_client.moveByRollPitchYawrateThrottleAsync(pitch=pitch_rate, roll=roll_rate, yaw_rate=yaw_rate,
                                                          throttle=throttle, duration=0.05)
    else:
        AirSim_client.hoverAsync()

    # 从 AirSim 客户端获取摄像头图像
    temp_image = AirSim_client.simGetImage('0', image_types["scene"])
    if temp_image is None:
        print("Warning: Failed to read a frame!! ")
        pygame.quit()
    else:
        pass

    # 加载图像并显示在屏幕上
    image = cv2.imdecode(airsim.string_to_uint8_array(temp_image), cv2.IMREAD_COLOR)
    screen_image = pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")
    screen.blit(screen_image, (0, 0))
    pygame.display.flip()
    pygame.display.update()
    #测距传感器
    data_distance = AirSim_client.getDistanceSensorData(vehicle_name="SimpleFlight")
    data_lidar = AirSim_client.getLidarData(vehicle_name="SimpleFlight")
    print(f"Distance & Lidar sensor data: Drone1: {data_distance.distance}")
    lidar_names = ['Lidar1', 'Lidar2']
    vehicle_name = "SimpleFlight"
    for lidar_name in lidar_names:
        filename = f"{vehicle_name}_{lidar_name}_pointcloud.asc"
        #指定存储目录
        file_path = os.path.join(data_path, filename)
        mode = 'w' if not existing_data_cleared else 'a'
        with open(file_path, mode) as f:
            lidar_data = AirSim_client.getLidarData(lidar_name=lidar_name, vehicle_name=vehicle_name)

            orientation = lidar_data.pose.orientation
            q0, q1, q2, q3 = orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val
            rotation_matrix = np.array(([1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q3 * q0), 2 * (q1 * q3 + q2 * q0)],
                                        [2 * (q1 * q2 + q3 * q0), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q1 * q0)],
                                        [2 * (q1 * q3 - q2 * q0), 2 * (q2 * q3 + q1 * q0),
                                         1 - 2 * (q1 * q1 + q2 * q2)]))

            position = lidar_data.pose.position
            for i in range(0, len(lidar_data.point_cloud), 3):
                xyz = lidar_data.point_cloud[i:i + 3]

                corrected_x, corrected_y, corrected_z = np.matmul(rotation_matrix, np.asarray(xyz))
                final_x = corrected_x + position.x_val
                final_y = corrected_y + position.y_val
                final_z = corrected_z + position.z_val

                f.write("%f %f %f \n" % (final_x, final_y, final_z))
            f.close()
    existing_data_cleared = True
    # 按下 'Esc' 键退出程序
    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()