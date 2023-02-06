import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


class Algorithm:

    def __init__(self, priority):
        self.priority = priority

    def run(self, light, distance):
        # Placeholder method to be overridden by derived classes
        pass


class EvitementObstacles(Algorithm):

    def run(self, light, distance):
        # Implement obstacle avoidance algorithm
        # Adjust priority based on distance sensor value
        self.priority = distance
        print("Running obstacle avoidance algorithm")


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


sa = SubsumptionArchitecture()
sa.add_algorithm(EvitementObstacles(2))
sa.add_algorithm(SuivreLumieres(1))
sa.run()
'''
class ObstacleAvoidance(Algorithm):
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
        priority_ctrl.add_rule(ctrl.Rule(distance['medium'], priority['medium']))
        priority_ctrl.add_rule(ctrl.Rule(distance['far'], priority['low']))

        # Simulate the fuzzy control system
        priority_sim = ctrl.ControlSystemSimulation(priority_ctrl)
        priority_sim.input['distance'] = distance
        priority_sim.compute()

        return priority_sim.output['priority']

class LightFollowing(Algorithm):
    def run(self, light, distance):
        # Implement light following algorithm
        # Adjust priority using fuzzy logic
        self.priority = self.fuzzy_priority(light)
        print("Running light following algorithm")

    def fuzzy_priority(self, light):
        # Define fuzzy membership functions for light
        light_bright = fuzz.trimf(np.arange(0, 100, 1), [0, 0, 50])
        light_medium = fuzz.trimf(np.arange(0, 100, 1), [0, 50, 100])
        light_dim = fuzz.trimf(np.arange(0, 100, 1), [50, 100, 100])

        # Define fuzzy control system
        priority_ctrl = ctrl.ControlSystem([
            ctrl.Consequent(np.arange(0, 2, 1), 'priority'),
            ctrl.Antecedent(np.arange(0, 100, 1), 'light')
        ])

        # Define fuzzy
         priority_ctrl.add_rule(ctrl.Rule(light['bright'], priority['high']))
    priority_ctrl.add_rule(ctrl.Rule(light['medium'], priority['medium']))
    priority_ctrl.add_rule(ctrl.Rule(light['dim'], priority['low']))

    # Simulate the fuzzy control system
    priority_sim = ctrl.ControlSystemSimulation(priority_ctrl)
    priority_sim.input['light'] = light
    priority_sim.compute()

    return priority_sim.output['priority']
def main():
obstacle_avoidance = ObstacleAvoidance(0)
light_following = LightFollowing(0)

python
Copy code
algorithms = [obstacle_avoidance, light_following]

# Example loop for reading sensory input from TCP/IP server
while True:
    # Read light and distance values from TCP/IP server
    light = 50
    distance = 25

    # Update priority of each algorithm based on sensory input
    for algorithm in algorithms:
        algorithm.run(light, distance)

    # Choose algorithm with highest priority
    highest_priority = max([algorithm.priority for algorithm in algorithms])
    chosen_algorithm = [algorithm for algorithm in algorithms if algorithm.priority == highest_priority][0]
    chosen_algorithm.run(light, distance)
if name == "main":
main()

This code demonstrates how to dynamically adjust the priority of two algorithms 
(obstacle avoidance and light following) based on sensory input (light and distance). 
The priority of each algorithm is computed using a fuzzy logic control system, which maps the sensory
input to a priority value. The algorithm with the highest priority is then executed.

'''
'''
 # Choose algorithm with highest priority
        highest_priority = max(
            [algorithm.priority for algorithm in algorithms])
        chosen_algorithm = [
            algorithm for algorithm in algorithms
            if algorithm.priority == highest_priority
        ][0]
        chosen_algorithm.run(light, distance)


def vote_coordination(light, distance):
    vote_weights = {'follow_light': 0, 'avoid_obstacles': 0}

    if light > 60:
        vote_weights['follow_light'] += 1
    if distance < 30:
        vote_weights['avoid_obstacles'] += 1

    return max(vote_weights, key=vote_weights.get)


'''