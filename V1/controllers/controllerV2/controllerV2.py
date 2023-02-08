"""braitenberg controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import numpy as np
import camera
import json
import socket

robot = Robot()

timestep = int(robot.getBasicTimeStep())

distanceSensors = [robot.getDevice(f"ds{i}") for i in range(8)]

light_sensors = [robot.getDevice(f"ls{i}") for i in range(8)]

for s in distanceSensors:
    s.enable(timestep)

for sensor in light_sensors:
    sensor.enable(timestep)

def sendSensorData(client, lightSensorValues, distanceSensorValues):
    data = {'light': lightSensorValues, 
    'distance': distanceSensorValues}
    data = json.dumps(data)
    client.send(data.encode(encoding='utf-8'))
    
weight_matrix = np.array([[-2, 4], [-3, 5], [-7, 7], [7, -6], [5, -4], [4, -2],
                          [-0.5, -0.5], [-0.5, -0.5]])

matrix = weight_matrix.tolist()

left_wheel = robot.getDevice("left wheel motor")
right_wheel = robot.getDevice("right wheel motor")
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))
left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

max_speed = left_wheel.getMaxVelocity()
speed_unit = 7
rangeSensor = distanceSensors[0].getMaxValue()

port = 10020
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"

def startup():
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.settimeout(30000)
    s.listen(1)
    print("Server {} listening on port {}".format(host, port))

startup()

left_wheel_speed = max_speed
right_wheel_speed = max_speed

while robot.step(timestep) != -1:
    c, addr = s.accept()
    print("Connection from", addr)
    sensorValues = [s.getValue() for s in distanceSensors]
    lightSensorValues = [l.getValue() for l in light_sensors]
    max_light_index = np.argmax(lightSensorValues)

    max_distance_sensor_value = max(sensorValues)
    max_distance_sensor_index = sensorValues.index(max_distance_sensor_value)
    sendSensorData(c, lightSensorValues, sensorValues)



    data = c.recv(1024)
    dataString = data.decode()
    speeds = data


    left_wheel.setVelocity(speeds[0])
    right_wheel.setVelocity(speeds[1])
