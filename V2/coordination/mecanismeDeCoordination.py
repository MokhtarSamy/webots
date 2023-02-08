import json
import socket

import requests


class Algorithm:

    def __init__(self):
        self.priority = 0

    def run(self):
        pass


class EvitementObstacles(Algorithm):
    name = "EvitementObstacles"

    def run(self, sensorValues):
        url = "http://127.0.0.1:5200/sensor"
        data = json.dumps(sensorValues)
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=data, headers=headers)
        request = requests.get('http://127.0.0.1:5200/speed')
        result = request.json()
        return 8, 8


class SuivreLumieres(Algorithm):
    name = "SuivreLumieres"

    def run(self, sensorValues):
        url = "http://127.0.0.1:5100/sensor"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(sensorValues)
        requests.post(url, data=data, headers=headers)
        request = requests.get("http://127.0.0.1:5100/speed")
        return 8, 8


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


def main():
    host = "host.docker.internal"
    port = 10020
    sa = SubsumptionArchitecture()
    sa.add_algorithm(EvitementObstacles())
    sa.add_algorithm(SuivreLumieres())

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        data = sock.recv(1024)
        dataString = data.decode()
        data = json.loads(dataString)
        lightValues = data['light']
        distanceValues = data['distance']
        speeds = sa.run(lightValues, distanceValues)
        sock.sendall(json.dumps(speeds).encode())


main()