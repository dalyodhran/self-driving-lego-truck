import tty
import sys
import termios
import motor
import data_collection

filedescriptors = termios.tcgetattr(sys.stdin)
x = 0


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
            motor.turnRight()
        if x == "D":
            motor.turnLeft()
        if x == 'r':
            print('Collecting Data')
            collect_data = True
        if x == 's':
            print('Saving colected Data')
            collect_data = False
            data_collection.save_collection()
        if collect_data:
            data_collection.collect_frame()

        x = 0

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)


if __name__ == '__main__':
    init()
    motor.run()
    control()
