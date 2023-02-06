"""braitenberg controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import numpy as np
import camera

robot = Robot()
# Initialize the robot
timestep = int(robot.getBasicTimeStep())

# Get the distance sensors
sensors = [robot.getDevice(f"ds{i}") for i in range(8)]

# Get the light sensors
light_sensors = [robot.getDevice(f"ls{i}") for i in range(8)]

# Enable the sensors
for s in sensors:
    s.enable(timestep)

# Enable light sensors
for sensor in light_sensors:
    sensor.enable(timestep)

weight_matrix = np.array([[-2, 4], [-3, 5], [-7, 7], [7, -6], [5, -4], [4, -2],
                          [-0.5, -0.5], [-0.5, -0.5]])
light_weight_matrix = np.array([0.9, 0.4, 0.3, 0.9, 0.4, 0.7, 0.9, 0.8])

# Get the wheels
left_wheel = robot.getDevice("left wheel motor")
right_wheel = robot.getDevice("right wheel motor")
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))
left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

max_speed = left_wheel.getMaxVelocity()
sensor_range = sensors[0].getMaxValue()

distance_target_value = 0.9
distance_kp = 0.5

while robot.step(timestep) != -1:
    # Get the sensor values
    sensorValues = [s.getValue() / sensor_range for s in sensors]
    sensorValues = [
        max(-max_speed, min(s, max_speed))
        for s in np.dot(sensorValues, weight_matrix)
    ]

    lightSensorValues = [s.getValue() for s in light_sensors]
    lightSensorValues = np.multiply(lightSensorValues, light_weight_matrix)
    max_light_index = np.argmax(lightSensorValues)

    # Find the sensor with the highest value
    max_distance_sensor_value = max(sensorValues)
    max_distance_sensor_index = sensorValues.index(max_distance_sensor_value)
    distance_error = max_distance_sensor_value - distance_target_value
    max_light_sensor_value = max(lightSensorValues)
    #max_light_sensor_argmax = lightSensorValues.argmax(max_light_sensor_value)
    #light_error = max_light_sensor_value - LIGHT_TARGET_VALUE

    # Calculate wheel speeds based on light error
    left_wheel_speed = max_speed
    right_wheel_speed = max_speed
    print(lightSensorValues)
    # If the max light sensor is on the left, adjust wheel speeds accordingly
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
