import json
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockLumieres = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockObstacles = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Algorithm:

    def __init__(self):
        self.priority = 0

    def run(self):
        pass


class EvitementObstacles(Algorithm):
    name = "EvitementObstacles"

    def run(self, sensorValues):
        sockObstacles.connect(("host.docker.internal", 5200))
        sensorValues = json.dumps(sensorValues)
        sockObstacles.sendall(sensorValues.encode(encoding='utf-8'))

        #client, addr = sockObstacles.accept()
        #sockObstacles.bind(("host.docker.internal", 5200))
        #conn, addr = sockObstacles.accept()
        data = sockObstacles.recv(1024)
        dataString = data.decode()
        data = json.loads(dataString)
        print("data obstacles: ", data)
        return data


class SuivreLumieres(Algorithm):
    name = "SuivreLumieres"

    def run(self, sensorValues):
        sockLumieres.connect(("host.docker.internal", 5100))
        sensorValues = json.dumps(sensorValues)
        sockLumieres.sendall(sensorValues.encode(encoding='utf-8'))

        #client, addr = sockObstacles.accept()
        #sockObstacles.bind(("host.docker.internal", 5200))
        #conn, addr = sockObstacles.accept()
        data = sockLumieres.recv(1024)
        dataString = data.decode()
        data = json.loads(dataString)
        print("data lumieres: ", data)
        return data


class SubsumptionArchitecture:

    def __init__(self):
        self.algorithms = []

    def add_algorithm(self, algorithm):
        self.algorithms.append(algorithm)
        #self.algorithms.sort(key=lambda x: x.priority, reverse=True)
    def update_priority(self, name):
        for algo in self.algorithms:
            if algo.name == name:
                algo.priority = 1
            else:
                algo.priority = 0

    def run(self, light, distance):
        # Sort algorithms by priority before running them
        if max(distance) > 900:
            self.update_priority('EvitementObstacles')
        else:
            self.update_priority('SuivreLumieres')
        self.algorithms.sort(key=lambda x: x.priority, reverse=True)
        if self.algorithms[0].name == 'EvitementObstacles':
            return self.algorithms[0].run(distance)
        else:
            return self.algorithms[0].run(light)


def get_sensor_values(host, port):
    # Create a TCP/IP socket

    sock.connect((host, port))
    print('Connected to {} port {}'.format(host, port))
    try:
        # Receive sensor values
        data = sock.recv(1024)
        dataString = data.decode()
        print("dataString: ", dataString)
        data = json.loads(dataString)
        lightValues = data['light']
        distanceValues = data['distance']

        #sensor_values = data.decode().replace('[', '').replace(']','').split(',')
        #for value in sensor_values:
        #   light.append(float(value[0]))
        #distance = float(sensor_values[1])
        return lightValues, distanceValues
    finally:
        print('Closing socket')
        sock.close()


def main():
    host = "host.docker.internal"
    #host = "127.0.0.1"
    port = 10020
    sa = SubsumptionArchitecture()
    while True:
        sa.add_algorithm(EvitementObstacles())
        sa.add_algorithm(SuivreLumieres())
        lightValues, distanceValues = get_sensor_values(host, port)
        sa.run(lightValues, distanceValues)


main()