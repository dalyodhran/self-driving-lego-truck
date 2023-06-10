import curses
import tty
import sys
import termios

import motor
from python.src.collection import data_collection
import threading
import time
import math
from pydualsense import *


# filedescriptors = termios.tcgetattr(sys.stdin)
# stop_threads = False
x = 0

def init():
    tty.setcbreak(sys.stdin)

def run():
    while True:
        data_collection.collect_frame()
        time.sleep(0.25)
        if stop_threads:
            print('Saving colected Data')
            data_collection.save_collection()
            break

def control():
    shouldRun = True
    while shouldRun:
        global stop_threads
        x = sys.stdin.read(1)[0]
        if x == "A":
            print("You pressed", x)
            motor.moveForward()
        if x == "B":
            print("You pressed", x)
            motor.stop()
        if x == "C":
            print("You pressed", x)
            motor.turnRight()
        if x == "D":
            print("You pressed", x)
            motor.turnLeft()
        if x == 'r':
            print("You pressed", x)
            print('Collecting Data')
            stop_threads = False
            # t1 = threading.Thread(target = run, daemon = True)
            # t1.start()
        if x == 's':
            print("You pressed", x)
            print('Saving colected Data')
            stop_threads = True

        x = 0

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)


def cross_down(state):
    if state:
        motor.moveForward()
    else:
        motor.stop()

    print(f'cross {state}')


def convert_thumbstick_input(x, y):
    # Calculate the angle of the thumbstick input
    angle = math.atan2(y, x)

    # Map the angle to a single axis value
    axis = math.cos(angle)

    return axis


def joystick(stateX, stateY):
    angle = convert_thumbstick_input(stateX, stateY)
    print(f'angle: {angle}')


def run_controller():

    while not dualsense.state.R1:

        if dualsense.state.circle:
            break


if __name__ == '__main__':
    init()
    dualsense = pydualsense()
    dualsense.init()

    while dualsense.states is None:
        print("Waiting until connection is established...")
        print(f"epoch: {time.time():.0f}")
        time.sleep(0.5)

    dualsense.cross_pressed += cross_down
    dualsense.left_joystick_changed += joystick
    run_controller()
    dualsense.close()

