import json
from flask import Flask, request

app = Flask(__name__)

sensorValues = []


@app.route('/sensor', methods=['POST'])
def updateSensor():
    global sensorValues
    data = request.get_data()
    sensorValues = data.decode('utf-8')


port = 5000
host = "coordination"


@app.route('/speed', methods=['GET'])
def suivreLumiere():
    global sensorValues
    max_speed = 10
    max_light_index = max(sensorValues)
    left_wheel_speed = 0
    right_wheel_speed = 0
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
    return {"left": left_wheel_speed, "right": right_wheel_speed}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5100)