from buildhat import MotorPair
from buildhat import Motor
import time
import math


# motor_forward = MotorPair('B', 'C')
# motor_forward.set_default_speed(100)
# motor_lr = Motor('A')
# lr_counter = 5
#
#
# def steer_to_prediction(steering):
#     transform_steering = (steering + 1) * 5
#     turns = int(math.ceil(transform_steering))
#     print(f'Turns: {turns}')
#     if turns > 5:
#         for i in range(0, turns):
#             turnRight()
#     else:
#         for i in range(5, turns):
#             turnLeft()
#
#
# def moveForward():
#     motor_forward.start()
#
#
# def turnLeft():
#     global lr_counter
#     if(lr_counter > 1):
#         motor_lr.run_for_degrees(-30)
#         lr_counter -= 1
#
#
# def turnRight():
#     global lr_counter
#     if(lr_counter < 9):
#         motor_lr.run_for_degrees(30)
#         lr_counter += 1
#
#
# def stop():
#     print("Stopping")
#     motor_forward.stop()
#
#
# def current_pos():
#     return (lr_counter / 5) - 1
#
#
#
#
# def run():
#     print("Calibrating")
#     calibrate()
#
#
# if __name__ == "__main__":
#     print("Calibrating")
#     calibrate()
#
#     print('Run test')
#     moveForward()
#     time.sleep(5)
#     stop()

class MotorImpl:

    motor_lr = Motor('A')
    center = 0
    abs_right = 0
    abs_left = 0

    def __init__(self):
        print("Calibrating")
        self.calibrate()

    def calibrate(self):
        avg_center = 0
        avg_right = 0
        avg_left = 0

        for i in range(0, 5):
            self.motor_lr.run_for_degrees(360)
            right_position = self.motor_lr.get_aposition()
            print(f'Fully right position {right_position}')

            self.motor_lr.run_for_degrees(-360)
            left_position = self.motor_lr.get_aposition()
            print(f'Fully left position {left_position}')

            offset = abs(right_position - left_position)
            if left_position > right_position:
                center_position = left_position + (offset / 2)
            else:
                center_position = right_position + (offset / 2)
            print(f'Center position {center_position}')

            avg_center += center_position
            avg_right += right_position
            avg_left += left_position

        self.center = avg_center // 5
        self.abs_right = avg_right // 5
        self.abs_left = avg_left // 5
        self.motor_lr.run_to_position(self.center)
        print(f'Average Center {self.center}')
        print(f'Average Right {self.abs_right}')
        print(f'Average Left {self.abs_left}')

    def go_to_position(self, value):
        self.motor_lr.run_to_position(value)


if __name__ == "__main__":
    motor = MotorImpl()
    input1 = input()
    while(True):
        motor.go_to_position(input1)
