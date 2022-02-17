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
            #collect_data = True
            data_collection.startCollecting()
        if x == 's':
            print("You pressed", x)
            print('Saving colected Data')
            #collect_data = False
            #data_collection.save_collection()
            data_collection.stopCollecting()
        if collect_data:
            data_collection.collect_frame()

        x = 0

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)


if __name__ == '__main__':
    init()
    motor.run()
    control()
