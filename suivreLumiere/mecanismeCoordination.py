'''
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 10020))

data = "N"
client.sendall(data.encode())

response = client.recv(1024).decode()
print("Response from server:", response.strip())



client.close()
'''
import json
import socket
import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz


class Algorithm:

    def __init__(self, priority):
        self.priority = priority

    def run(self, light, distance):
        # Placeholder method to be overridden by derived classes
        pass


class EvitementObstacles(Algorithm):

    def run(self, light, distance):
        # Implement obstacle avoidance algorithm
        # Adjust priority using fuzzy logic
        self.priority = self.fuzzy_priority(distance)
        print("Running obstacle avoidance algorithm")

    def fuzzy_priority(self, distance):
        # Define fuzzy membership functions for distance
        distance_near = fuzz.trimf(np.arange(0, 50, 1), [0, 0, 25])
        distance_medium = fuzz.trimf(np.arange(0, 50, 1), [0, 25, 50])
        distance_far = fuzz.trimf(np.arange(0, 50, 1), [25, 50, 50])

        # Define fuzzy control system
        priority_ctrl = ctrl.ControlSystem([
            ctrl.Consequent(np.arange(0, 2, 1), 'priority'),
            ctrl.Antecedent(np.arange(0, 50, 1), 'distance')
        ])

        # Define fuzzy rules
        priority_ctrl.add_rule(ctrl.Rule(distance['near'], priority['high']))
        priority_ctrl.add_rule(
            ctrl.Rule(distance['medium'], priority['medium']))
        priority_ctrl.add_rule(ctrl.Rule(distance['far'], priority['low']))

        # Simulate the fuzzy control system
        priority_sim = ctrl.ControlSystemSimulation(priority_ctrl)
        priority_sim.input['distance'] = distance
        priority_sim.compute()

        return priority_sim.output['priority']


class SuivreLumieres(Algorithm):

    def run(self, light, distance):
        # Implement light following algorithm
        # Adjust priority based on light sensor value
        self.priority = light
        print("Running light following algorithm")


class SubsumptionArchitecture:

    def __init__(self):
        self.algorithms = []

    def add_algorithm(self, algorithm):
        self.algorithms.append(algorithm)
        #self.algorithms.sort(key=lambda x: x.priority, reverse=True)

    def run(self, light, distance):
        # Sort algorithms by priority before running them
        self.algorithms.sort(key=lambda x: x.priority, reverse=True)
        for algorithm in self.algorithms:
            if algorithm.run(light, distance):
                break


def get_sensor_values(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Connecting to {} port {}'.format(host, port))
    sock.connect((host, port))

    try:
        # Send request for sensor values
        '''message = 'REQUEST_SENSOR_VALUES'
        message = message.encode('utf-8')
        print('Sending: {}'.format(message))
        sock.send(message)'''
        # Receive sensor values
        data = sock.recv(1024)
        dataString = data.decode()
        lightSensorValues = json.loads(dataString)
        #sensor_values = data.decode().replace('[', '').replace(']','').split(',')
        #for value in sensor_values:
        #   light.append(float(value[0]))
        #distance = float(sensor_values[1])
        print('Received: {}'.format(lightSensorValues))
        return lightSensorValues
    finally:
        print('Closing socket')
        sock.close()


def main():
    host = "host.docker.internal"
    port = 10020
    sa = SubsumptionArchitecture()

    while True:
        light = get_sensor_values(host, port)
        sa.add_algorithm(EvitementObstacles(2))
        sa.add_algorithm(SuivreLumieres(1))
        sa.run()


if __name__ == "__main__":
    main()
'''
def vote_coordination(light, distance):
    vote_weights = {'follow_light': 0, 'avoid_obstacles': 0}

    if light > 60:
        vote_weights['follow_light'] += 1
    if distance < 30:
        vote_weights['avoid_obstacles'] += 1

    return max(vote_weights, key=vote_weights.get)

'''