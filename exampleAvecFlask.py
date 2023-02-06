from flask import Flask, request

app = Flask(__name__)

light = 50
distance = 20


@app.route('/sensor_values', methods=['GET'])
def sensor_values():
    global light, distance
    return '{},{}'.format(light, distance)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)

#CLIENT
import requests


def get_sensor_values(host, port):
    url = 'http://{}:{}/sensor_values'.format(host, port)
    response = requests.get(url)
    sensor_values = response.text.split(',')
    light = int(sensor_values[0])
    distance = int(sensor_values[1])

    return light, distance
