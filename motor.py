from buildhat import MotorPair
from buildhat import Motor
import time


motor_forward = MotorPair('B', 'C')
motor_forward.set_default_speed(100)
motor_lr = Motor('A')
global_left_rotate = 0
global_right_rotate = 0

def moveForward():
    motor_forward.start()


def turnLeft(deg):
    currentDeg = motor_lr.get_aposition()
    if(currentDeg + deg > global_left_rotate):
        motor_lr.run_for_degrees(global_left_rotate-currentDeg)
    else:
        motor_lr.run_for_degrees(deg)


def turnRight(deg):
    currentDeg = motor_lr.get_aposition()
    if(currentDeg + deg < global_right_rotate):
        motor_lr.run_for_degrees(global_right_rotate-currentDeg)
    else:
        motor_lr.run_for_degrees(deg)
    motor_lr.run_for_degrees(deg)


def stop():
    print("Stopping")
    motor_forward.stop()


def current_pos():
    return motor_lr.get_aposition()


def calibrate():
    avg_center = 0
    avg_left = 0
    avg_right = 0
    for i in range(0, 5):
        motor_lr.run_for_degrees(360)

        position_right = motor_lr.get_aposition()
        avg_right = avg_right + position_right
        print(position_right)

        motor_lr.run_for_degrees(-360)
        position_left = motor_lr.get_aposition()
        avg_left = avg_left + position_left
        print(position_left)
        offset = abs(position_right - position_left)
        if position_left > position_right:
            center = position_left + (offset/2)
        else:
            center = position_right + (offset/2)
        print(f'center: {center}')
        avg_center += center

    motor_lr.run_to_position(avg_center/5)
    global_left_rotate = avg_left/5
    global_right_rotate = avg_right/5
    print(motor_lr.get_aposition())


def run():
    print("Calibrating")
    calibrate()


if __name__ == "__main__":
    print("Calibrating")
    calibrate()

    print('Run test')
    moveForward()
    time.sleep(5)
    stop()
