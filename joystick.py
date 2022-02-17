from math import fabs
import tty
import sys
import termios
import motor
import data_collection as dc

x = 0
filedescriptors = termios.tcgetattr(sys.stdin)


def init():
    tty.setcbreak(sys.stdin)


def control():
    collect_data = False
    while 1:
        x = sys.stdin.read(1)[0]
        print("You pressed", x)
        if x == "A":
            motor.moveForward()
        if x == "B":
            motor.stop()
        if x == "C":
            motor.turnRight(30)
        if x == "D":
            motor.turnLeft(-30)
        if x == 'r':
            print('Collecting Data')
            collect_data = True
        if x == 's':
            print('Saving colected Data')
            collect_data = False
            dc.save_collection()

        if collect_data:
            dc.collect_frame()

        x = "G"

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)


if __name__ == '__main__':
    init()
    motor.run()
    control()
