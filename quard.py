import airsim
import time

# 连接到 AirSim 仿真器
client = airsim.MultirotorClient()

client.enableApiControl(True)   # 获取控制权
client.armDisarm(True)          # 解锁
client.takeoffAsync().join()    # 起飞

# 方形飞行路径
client.moveToZAsync(-0.5, 1).join()               # 上升到3m高度
#client.moveToPositionAsync(5, 0, -3, 1).join()  # 飞到（5,0）点坐标
#client.moveToPositionAsync(5, 5, -3, 1).join()  # 飞到（5,5）点坐标
#client.moveToPositionAsync(0, 5, -3, 1).join()  # 飞到（0,5）点坐标
#client.moveToPositionAsync(0, 0, -3, 1).join()  # 回到（0,0）点坐标

#client.landAsync().join()       # 降落
#client.armDisarm(False)         # 上锁
#client.enableApiControl(False)  # 释放控制权
