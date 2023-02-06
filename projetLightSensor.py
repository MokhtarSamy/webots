"""braitenberg controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import numpy as np
import camera

robot = Robot()
# Initialize the robot
timestep = int(robot.getBasicTimeStep())
#print(robot.getName())

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

light_weight_matrix = np.array([0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])

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

light_target_value = 0.6
light_kp = 0.3

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

    # Find the sensor with the highest value
    max_distance_sensor_value = max(sensorValues)
    max_distance_sensor_index = sensorValues.index(max_distance_sensor_value)
    distance_error = max_distance_sensor_value - distance_target_value

    max_light_sensor_value = max(lightSensorValues)
    #max_light_sensor_argmax = lightSensorValues.argmax(max_light_sensor_value)
    light_error = max_light_sensor_value - light_target_value
    # Adjust the speed of the wheels based on the errors
    left_wheel_speed = light_kp * light_error
    right_wheel_speed = light_kp * light_error
    print(lightSensorValues)

    left_wheel.setVelocity(left_wheel_speed)
    right_wheel.setVelocity(right_wheel_speed)
