weight_matrix = [[-2, 4], [-3, 5], [-7, 7], [7, -6], [5, -4], [4, -2],
                 [-0.5, -0.5], [-0.5, -0.5]]
speed_unit = 7
max_speed = 10


def bound(x, a, b):
    return min(max(x, a), b)


def avoid_obstacles(sensorsValues):
    speed = [0.0, 0.0]
    print(sensorsValues)
    for i in range(2):
        for j in range(8):
            speed[i] += speed_unit * weight_matrix[j][i] * (
                1.0 - (sensorsValues[j] / 1023))
        speed[i] = bound(speed[i], -max_speed, max_speed)
    if min(speed[0], speed[1]) < 0:
        speed[0] = -max_speed
        speed[1] = -max_speed
    return speed