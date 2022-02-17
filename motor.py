from buildhat import MotorPair
from buildhat import Motor
import time


motor_forward = MotorPair('B', 'C')
motor_forward.set_default_speed(100)
motor_lr = Motor('A')


def moveForward():
    motor_forward.start()


def turnLeft(deg):
    motor_lr.run_for_degrees(deg)


def turnRight(deg):
    motor_lr.run_for_degrees(deg)


def stop():
    print("Stopping")
    motor_forward.stop()


def current_pos():
    return motor_lr.get_aposition()


def calibrate():
    avg_center = 0

    for i in range(0, 5):
        motor_lr.run_for_degrees(360)

        position_right = motor_lr.get_aposition()
        print(position_right)

        motor_lr.run_for_degrees(-360)
        position_left = motor_lr.get_aposition()
        print(position_left)
        offset = abs(position_right - position_left)
        if position_left > position_right:
            center = position_left + (offset/2)
        else:
            center = position_right + (offset/2)
        print(f'center: {center}')
        avg_center += center

    motor_lr.run_to_position(avg_center/5)
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
