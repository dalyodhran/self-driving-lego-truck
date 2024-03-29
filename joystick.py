import tty
import sys
import termios
import motor
import data_collection
import threading
import time

filedescriptors = termios.tcgetattr(sys.stdin)
stop_threads = False
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
            t1 = threading.Thread(target = run, daemon = True)
            t1.start()
        if x == 's':
            print("You pressed", x)
            print('Saving colected Data')
            stop_threads = True

        x = 0

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)


if __name__ == '__main__':
    init()
    motor.run()
    control()
