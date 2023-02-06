"""braitenberg controller. version qui fonctionne bien comme serveur Webots"""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import numpy as np
import camera
import socket
import select
import json

robot = Robot()
# Initialize the robot
timestep = int(robot.getBasicTimeStep())
#print(robot.getName())

# Get the distance sensors
distanceSensors = [robot.getDevice(f"ds{i}") for i in range(8)]

# Get the light sensors
light_sensors = [robot.getDevice(f"ls{i}") for i in range(8)]

# Enable the sensors
for s in distanceSensors:
    s.enable(timestep)

# Enable light sensors
for sensor in light_sensors:
    sensor.enable(timestep)

weight_matrix = np.array([[-2, 4], [-3, 5], [-7, 7], [7, -6], [5, -4], [4, -2],
                          [-0.5, -0.5], [-0.5, -0.5]])

# Get the wheels
left_wheel = robot.getDevice("left wheel motor")
right_wheel = robot.getDevice("right wheel motor")
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))
left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

max_speed = left_wheel.getMaxVelocity()
sensor_range = sensors[0].getMaxValue()
#print(f"{max_speed = } | {sensor_range = }

distance_target_value = 0.9
distance_kp = 0.5
port = 10020
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"


def startup():
    # -- Called during worker process start up sequence
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.settimeout(30000)
    s.listen(1)
    print("Server {} listening on port {}".format(host, port))


startup()
#c, addr = s.accept()
#print("Accepted connection from: {}".format(addr[0]))


def send_sensor_data(client, lightSensorValues):
    lightSensorValues = json.dumps(lightSensorValues)
    client.send(lightSensorValues.encode(encoding='utf-8'))


left_wheel_speed = max_speed
right_wheel_speed = max_speed

while robot.step(timestep) != -1:
    c, addr = s.accept()
    print("Connection from", addr)
    #handle_request(data)
    # send sensor data to client
    # Get the sensor values
    sensorValues = [s.getValue() / sensor_range for s in sensors]
    sensorValues = [
        max(-max_speed, min(s, max_speed))
        for s in np.dot(sensorValues, weight_matrix)
    ]

    lightSensorValues = [l.getValue() for l in light_sensors]
    #lightSensorValues = np.multiply(lightSensorValues, light_weight_matrix)
    send_sensor_data(c, lightSensorValues)
    max_light_index = np.argmax(lightSensorValues)

    # Find the sensor with the highest value
    max_distance_sensor_value = max(sensorValues)
    max_distance_sensor_index = sensorValues.index(max_distance_sensor_value)
    distance_error = max_distance_sensor_value - distance_target_value
    max_light_sensor_value = max(lightSensorValues)
    #max_light_sensor_argmax = lightSensorValues.argmax(max_light_sensor_value)
    #light_error = max_light_sensor_value - LIGHT_TARGET_VALUE

    # Calculate wheel speeds based on light error

    #print(lightSensorValues)
    # If the max light sensor is on the left, adjust wheel speeds accordingly
    #print(lightSensorValues)

    print("LEFT ", left_wheel_speed)
    print(" RIGHT ", right_wheel_speed)
    print(" SENSOR ", lightSensorValues)
    print(" MAX  ", max_light_index)
    if max_light_index == 0:
        left_wheel_speed = max_speed
        right_wheel_speed = max_speed * 0.5
    elif max_light_index == 1:
        left_wheel_speed = max_speed
        right_wheel_speed = max_speed * 0.6
    elif max_light_index == 2:
        left_wheel_speed = max_speed
        right_wheel_speed = max_speed * 0.7
    elif max_light_index == 3:
        left_wheel_speed = max_speed
        right_wheel_speed = max_speed * 0.8
    elif max_light_index == 4:
        left_wheel_speed = max_speed * 0.8
        right_wheel_speed = max_speed
    elif max_light_index == 5:
        left_wheel_speed = max_speed * 0.7
        right_wheel_speed = max_speed
    elif max_light_index == 6:
        left_wheel_speed = max_speed * 0.6
        right_wheel_speed = max_speed
    elif max_light_index == 7:
        left_wheel_speed = max_speed * 0.5
        right_wheel_speed = max_speed

    left_wheel.setVelocity(left_wheel_speed)
    right_wheel.setVelocity(right_wheel_speed)
