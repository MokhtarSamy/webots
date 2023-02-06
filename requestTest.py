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


def get_sensor_values(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = (host, port)
    print('Connecting to {} port {}'.format(server_address))
    sock.connect(server_address)

    try:
        # Send request for sensor values
        '''message = 'REQUEST_SENSOR_VALUES'
        message = message.encode('utf-8')
        print('Sending: {}'.format(message))
        sock.send(message)'''
        light = []
        # Receive sensor values
        data = sock.recv(1024)
        print("THIS IS DATA ", data)
        dataString = data.decode()
        lightSensorValues = json.loads(dataString)
        print("THIS IS DATA ", type(data))
        #sensor_values = data.decode().replace('[', '').replace(']','').split(',')
        #for value in sensor_values:
        #   light.append(float(value[0]))
        #distance = float(sensor_values[1])
        print('Received: {}'.format(lightSensorValues))
        return lightSensorValues, 0
    finally:
        print('Closing socket')
        sock.close()


def main():
    host = '127.0.0.1'
    port = 10020

    while True:
        light, distance = get_sensor_values(host, port)
        #print('Light: {}, Distance: {}'.format(light, distance))


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