import json
import socket

max_speed = 10
port = 5000
host = "coordination"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def suivreLumiere(sensorValues, max_speed):
    max_light_index = max(sensorValues)
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
    return left_wheel_speed, right_wheel_speed


def connect():
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.settimeout(30000)
    s.listen()


def sendSpeed():
    s.connect((host, port))
    conn, addr = s.accept()
    data = conn.recv(1024)
    sensorValues = json.dumps(data)
    speed = suivreLumiere(sensorValues, max_speed)
    conn.sendall(speed)


#connect()
sendSpeed()
