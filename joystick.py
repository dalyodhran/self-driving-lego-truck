import tty
import sys
import motor
import data_collection
import time
from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice('/dev/input/event0')
import fpstimer

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

absolutes = {
    0: 'left joystick left/right',
    1: 'left joystick up/down'
}

CENTER = 128
BLIND = 6
left_joystick = [CENTER, CENTER]

def update_left_joystick_position(event):
    global left_joystick
    if event.code == 0:
        left_joystick[0] = value
    elif event.code == 1:
        left_joystick[1] = value


if __name__ == '__main__':
    init()
    # motor.run()
    # control()

    print(gamepad)
    timer = fpstimer.FPSTimer(30)

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS and event.code in absolutes:
            action, value = absolutes[event.code], event.value

            if event.code in [0, 1]:
                if event.code in [0, 1]:
                    update_left_joystick_position(event)

                if (CENTER - BLIND) < event.value < (CENTER + BLIND):
                    continue

                print(f'{left_joystick}')
                continue

        timer.sleep()
