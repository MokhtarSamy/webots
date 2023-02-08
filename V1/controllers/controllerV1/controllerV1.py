"""braitenberg controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import numpy as np
import camera
import json


class Algorithm:

    def __init__(self):
        self.priority = 0

    def run(self):
        pass


class EvitementObstacles(Algorithm):
    name = "EvitementObstacles"

    def run(self, sensorValues):
        return avoid_obstacles(sensorValues)


class SuivreLumieres(Algorithm):
    name = "SuivreLumieres"

    def run(self, sensorValues):
        return follow_light(sensorValues)


class SubsumptionArchitecture:

    def __init__(self):
        self.algorithms = []

    def add_algorithm(self, algorithm):
        self.algorithms.append(algorithm)

    def update_priority(self, name):
        for algo in self.algorithms:
            if algo.name == name:
                algo.priority = 1
            else:
                algo.priority = 0

    def run(self, light, distance):
        if max(distance) > 900:
            self.update_priority('EvitementObstacles')
        else:
            self.update_priority('SuivreLumieres')
        self.algorithms.sort(key=lambda x: x.priority, reverse=True)
        if self.algorithms[0].name == 'EvitementObstacles':
            return self.algorithms[0].run(distance)
        else:
            return self.algorithms[0].run(light)


robot = Robot()
timestep = int(robot.getBasicTimeStep())

distanceSensors = [robot.getDevice(f"ds{i}") for i in range(8)]

light_sensors = [robot.getDevice(f"ls{i}") for i in range(8)]

for s in distanceSensors:
    s.enable(timestep)

for sensor in light_sensors:
    sensor.enable(timestep)

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

distance_target_value = 0.9
distance_kp = 0.5
baseSpeed = 4.0

k = 2.0

b = 0.1

left_wheel_speed = max_speed
right_wheel_speed = max_speed


def bound(x, a, b):
    return min(max(x, a), b)


def avoid_obstacles(sensorsValues):
    speed = [0.0, 0.0]
    print(sensorsValues)
    for i in range(2):
        for j in range(8):
            speed[i] += speed_unit * weight_matrix[j][i] * (
                1.0 - (sensorsValues[j] / rangeSensor))
        speed[i] = bound(speed[i], -max_speed, max_speed)
    if min(speed[0], speed[1]) < 0:
        speed[0] = -max_speed
        speed[1] = -max_speed
    return speed


def avoid_obstaclesV2(sensorValues):
    leftSpeed = baseSpeed
    rightSpeed = baseSpeed

    for i in range(8):
        readings = sensorValues[i]
        if i == 0 or i == 7:
            leftSpeed += k * readings
        elif i == 1 or i == 6:
            leftSpeed += k * readings / 2
            rightSpeed += k * readings / 2
        elif i == 2 or i == 5:
            rightSpeed += k * readings
        elif i == 3:
            leftSpeed -= k * readings / 2
            rightSpeed += k * readings / 2
        elif i == 4:
            leftSpeed += k * readings / 2
            rightSpeed -= k * readings / 2
    if min(leftSpeed, rightSpeed) < 0:
        leftSpeed = -baseSpeed
        rightSpeed = -baseSpeed
    return leftSpeed, rightSpeed


def braitenberg_algorithm(sensor_values):
    left_wheel_speed = 0
    right_wheel_speed = 0
    if sensor_values[0] != 0.0 and sensor_values[1] != 0.0:
        for i in range(8):
            sensor_value = sensor_values[i]

            if i < 4:
                left_wheel_speed += sensor_value
                right_wheel_speed -= sensor_value
            else:
                left_wheel_speed -= sensor_value
                right_wheel_speed += sensor_value

        if max_speed > 0:
            left_wheel_speed /= max_speed
            right_wheel_speed /= max_speed
    else:
        left_wheel_speed = max_speed
        right_wheel_speed = max_speed
    return left_wheel_speed, right_wheel_speed


def follow_light(lightSensorValues):
    max_light_sensor_value = max(lightSensorValues)
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
    return left_wheel_speed, right_wheel_speed


while robot.step(timestep) != -1:

    sensorValues = [s.getValue() for s in distanceSensors]
    lightSensorValues = [l.getValue() for l in light_sensors]
    max_light_index = np.argmax(lightSensorValues)

    max_distance_sensor_value = max(sensorValues)
    max_distance_sensor_index = sensorValues.index(max_distance_sensor_value)
    distance_error = max_distance_sensor_value - distance_target_value

    speeds = [6.0, 6.0]
    coordination = SubsumptionArchitecture()
    coordination.add_algorithm(EvitementObstacles())
    coordination.add_algorithm(SuivreLumieres())
    speeds = coordination.run(lightSensorValues, sensorValues)

    left_wheel.setVelocity(speeds[0])
    right_wheel.setVelocity(speeds[1])
