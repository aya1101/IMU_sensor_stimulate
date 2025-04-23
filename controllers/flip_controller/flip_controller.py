from controller import Robot
import math
import csv

robot = Robot()
timestep = int(robot.getBasicTimeStep())

imu = robot.getDevice("imu_sensor")
if imu is None:
    print("Error: IMU 'imu_sensor' not found!")
    exit()
imu.enable(timestep)

data = []
t = 0
T = 1.0

while robot.step(timestep) != -1:
    if t <= T:
        angle = math.pi * (t / T)
        node = robot.getFromDef("BOX")
        if node is None:
            print("Error: Node 'BOX' not found!")
            exit()
        node.getField("rotation").setSFRotation([1, 0, 0, angle])

        acc = imu.getAccelerometerValues()
        gyro = imu.getGyroValues()
        data.append([t, acc[0], acc[1], acc[2], gyro[0], gyro[1], gyro[2]])

        t += timestep / 1000.0
    else:
        break

with open("imu_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"])
    writer.writerows(data)

print("Simulation completed!")
