from buildhat import MotorPair
from buildhat import Motor
import time
import math

# lr_counter = 5


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
#         print(f'Before turn {motor_lr.get_position()}')
#         motor_lr.run_for_degrees(-30)
#         print(f'Before turn {motor_lr.get_position()}')
#         lr_counter -= 1
#
#
# def turnRight():
#     global lr_counter
#     if(lr_counter < 9):
#         print(f'Before turn {motor_lr.get_position()}')
#         motor_lr.run_for_degrees(30)
#         print(f'Before turn {motor_lr.get_position()}')
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
# def calibrate():
#     avg_center = 0
#     for i in range(0, 5):
#         motor_lr.run_for_degrees(360)
#
#         position_right = motor_lr.get_aposition()
#         print(position_right)
#
#         motor_lr.run_for_degrees(-360)
#         position_left = motor_lr.get_aposition()
#         print(position_left)
#         offset = abs(position_right - position_left)
#         if position_left > position_right:
#             center = position_left + (offset/2)
#         else:
#             center = position_right + (offset/2)
#         print(f'center: {center}')
#         avg_center += center
#
#     motor_lr.run_to_position(avg_center/5)
#     print(motor_lr.get_aposition())
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


class LegoMotor:
    motor_forward = MotorPair('B', 'C')
    motor_forward.set_default_speed(100)
    motor_lr = Motor('A')
    avg_center = 0
    avg_left = 0
    avg_right = 0
    controller_max_left = -32767
    controller_max_right = 32767
    left_multiplier = 0
    right_multiplier = 0

    def __init__(self):
        print("Calibrating")
        self.calibrate()
        self.left_multiplier = self.controller_max_left // self.avg_left
        print(f'Left turn multiplier {self.left_multiplier}')
        self.right_multiplier = self.controller_max_right // self.avg_right
        print(f'Right turn multiplier {self.right_multiplier}')

    def turn_right(self, value):
        turn_value = value // self.right_multiplier
        print(f'Right turn value {turn_value}')
        self.motor_lr.run_to_position(turn_value)

    def turn_left(self, value):
        turn_value = value // self.left_multiplier
        print(f'left turn value {turn_value}')
        self.motor_lr.run_to_position(turn_value)

    def calibrate(self):
        for i in range(0, 5):
            self.motor_lr.run_for_degrees(360)
            position_right = self.motor_lr.get_aposition()
            print(position_right)

            self.motor_lr.run_for_degrees(-360)
            position_left = self.motor_lr.get_aposition()
            print(position_left)

            offset = abs(position_right - position_left)

            if position_left > position_right:
                center = position_left + (offset / 2)
            else:
                center = position_right + (offset / 2)
            print(f'center: {center}')
            self.avg_center += center
            self.avg_left += position_left
            self.avg_right += position_right

        self.motor_lr.run_to_position(self.avg_center / 5)
        self.avg_left = self.avg_left // 5
        self.avg_right = self.avg_right // 5

        print(f'Average left {self.avg_left}')
        print(f'Average right {self.avg_right}')
        print(self.motor_lr.get_aposition())
