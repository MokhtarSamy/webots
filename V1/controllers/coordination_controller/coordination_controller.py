"""braitenberg controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import numpy as np
import math

robot = Robot()
# Initialize the robot
timestep = int(robot.getBasicTimeStep())
#print(robot.getName())

class ObstacleAvoidanceController:
    def __init__(self, robot):
        self.robot = robot
        self.speed = 1.0                
        # Get the distance sensors
        self.sensors = [robot.getDevice(f"ds{i}") for i in range(8)]
        
        # Enable the sensors
        for s in self.sensors:
            s.enable(timestep)
            
        self.max_dist = self.sensors[0].getMaxValue()
            
        self.left_wheel = robot.getDevice("left wheel motor")
        self.right_wheel = robot.getDevice("right wheel motor")
        self.left_wheel.setPosition(float('inf'));
        self.right_wheel.setPosition(float('inf'));
        
        self.max_velocity = self.left_wheel.getMaxVelocity()
        
        self.weight_matrix = np.array([[-2, 4], [-3, 5], [-7, 7], [7, -6], [5, -4], [4, -2], [-0.5, -0.5], [-0.5, -0.5]]);

    def step(self):
        distances = np.array([1.0 - (s.getValue() / self.max_dist) for s in self.sensors])
        
        speed = (distances @ self.weight_matrix) * self.speed
        
        max_speed = max(map(abs,speed))
        
        applied_factor = min(1, self.max_velocity / max_speed)
        
        speed *= applied_factor
        
        self.left_wheel.setVelocity(speed[0])
        self.right_wheel.setVelocity(speed[1])
        
        
class LightFollower:
    def __init__(self, robot):
        self.light_sensors = []
        self.motor_speeds = []
        self.num_sensors = 8
        self.speed = 2.0

        for i in range(self.num_sensors):
            light_sensor = robot.getDevice(f"ls{i}")
            light_sensor.enable(timestep)
            self.light_sensors.append(light_sensor)
            
        print(f"{self.light_sensors[0].getLookupTable()=}")
            
        self.left_motor = robot.getDevice("left wheel motor")
        self.right_motor = robot.getDevice("right wheel motor")

        # Configuration des moteurs en mode de contrôle de vitesse
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        
        self.max_velocity = self.left_motor.getMaxVelocity()
        
        # Matrice de poids pour les moteurs gauche et droit
        self.weight_matrix = np.array(
            [[-5, 0], [0, 5], [9, 10], [10, 10], [10, 10], [10, 9], [5, 0], [0, -5]]
        );


    def step(self):
        light_values = np.array([sensor.getValue() for sensor in self.light_sensors])
        
        max_idx = np.argmax(light_values)
        
        speed = self.weight_matrix[max_idx]
       
        print(f"{speed=}")
        
        self.left_motor.setVelocity(speed[0])
        self.right_motor.setVelocity(speed[1])


class Coordination:
    def __init__(self, light_behavior, obstacle_behavior, threshold):
        self.light_behavior = light_behavior
        self.obstacle_behavior = obstacle_behavior
        self.threshold = threshold
  
        # Get the distance sensors
        self.sensors = obstacle_behavior.sensors
    
    def step(self):
        dist_values = (sensor.getValue() for sensor in self.sensors if sensor.getValue() != 0.0)
        min_dist = min(dist_values, default=self.threshold)
        
        if min_dist < self.threshold:
            self.obstacle_behavior.step()
        else:
            self.light_behavior.step()

obstacle_avoidance_controller = ObstacleAvoidanceController(robot)
light_follower_controller = LightFollower(robot)
coordination_controller = Coordination(light_follower_controller, obstacle_avoidance_controller, 600.0);

while robot.step(timestep) != -1:
    coordination_controller.step()
