def suivreLumiere(max_light_index, max_speed):
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
