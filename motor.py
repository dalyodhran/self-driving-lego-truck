from buildhat import MotorPair
from buildhat import Motor
import time
import math


motor_forward = MotorPair('C', 'D')
# motor_forward.set_default_speed(100)
# motor_lr = Motor('A')
# lr_counter = 5


def steer_to_prediction(steering):
    transform_steering = (steering + 1) * 5
    turns = int(math.ceil(transform_steering))
    print(f'Turns: {turns}')
    if turns > 5:
        for i in range(0, turns):
            turnRight()
    else:
        for i in range(5, turns):
            turnLeft()


def moveForward():
    motor_forward.start()
    print("Moving Forward")


def turnLeft():
    global lr_counter
    if(lr_counter > 1):
        # motor_lr.run_for_degrees(-30)
        print("turning left")
        lr_counter -= 1


def turnRight():
    global lr_counter
    if(lr_counter < 9):
        # motor_lr.run_for_degrees(30)
        print("turning right")
        lr_counter += 1


def stop():
    print("Stopping")
    motor_forward.stop()


def current_pos():
    return (lr_counter / 5) - 1


def calibrate():
    avg_center = 0
    # for i in range(0, 5):
        # motor_lr.run_for_degrees(360)

        # position_right = motor_lr.get_aposition()
        # print(position_right)
        #
        # motor_lr.run_for_degrees(-360)
        # position_left = motor_lr.get_aposition()
        # print(position_left)
        # offset = abs(position_right - position_left)
        # if position_left > position_right:
        #     center = position_left + (offset/2)
        # else:
        #     center = position_right + (offset/2)
        # print(f'center: {center}')
        # avg_center += center

    # motor_lr.run_to_position(avg_center/5)
    # print(motor_lr.get_aposition())


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
