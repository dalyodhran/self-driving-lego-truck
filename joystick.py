import tty, sys, termios
import motor

x=0
filedescriptors = termios.tcgetattr(sys.stdin)

def init():
  tty.setcbreak(sys.stdin)
  motor.calibrate()

def control():
    while 1:
        x=sys.stdin.read(1)[0]
        print("You pressed", x)
        if x == "A":
            motor.moveForward()
        if x == "B":
            motor.stop()
        if x == "C":
            motor.turnRight(30)
        if x == "D":
            motor.turnLeft(30)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)

 
if __name__ == '__main__':
    init()
    while True:
        control()
