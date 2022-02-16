from buildhat import MotorPair
from buildhat import Motor
import time
#74, -126
motor_forward = MotorPair('B','C')
motor_forward.set_default_speed(50)
motor_lr = Motor('A')
top = 0
bottom = 0
center = 0
currentDeg = 0

def moveForward():
	motor_forward.start()

def Forward(go = True):
    while (go):
        motor_forward.run_for_seconds(0.1)

def turnLeft(deg):
   # endDeg = currentDeg + deg
   # if(endDeg>25):
   #     endDeg = 25

    #moveDeg = endDeg - currentDeg

    #points = (bottom,-25),(top,25),(ePos,moveDeg)
   # ePos = bottom + ((moveDeg + 25)/(25 + 25))*(top - bottom)

    #movePos = ePos - motor_lr.get_position()

    motor_lr.run_for_degrees(-deg)

def turnRight(deg):
    #endDeg = currentDeg - deg
    #if(endDeg<-25):
     #   endDeg = -25

   # moveDeg = endDeg - currentDeg

    #points = (bottom,-25),(top,25),(ePos,moveDeg)
    #ePos = bottom + ((moveDeg + 25)/(25 + 25))*(top - bottom)

    #movePos = ePos - motor_lr.get_position()

    motor_lr.run_for_degrees(deg)

def stop():
    print("Stopping")
    motor_forward.stop()

def straighten():
    global currentDeg
    print(center)
    motor_lr.run_for_degrees(convert_num(center) - motor_lr.get_position())
    currentDeg = current_pos()

def calibrate():
    global center,top,bottom,currentDeg
    motor_lr.run_for_degrees(-300)
    top = convert_num(motor_lr.get_position())
    motor_lr.run_for_degrees(600)
    bottom = convert_num(motor_lr.get_position())
    offset = abs(top-bottom)
    if(top>bottom):
        center = bottom + (offset/2)
    else:
        center = top + (offset/2)

    print(top,bottom,offset,center)
    currentDeg = current_pos()

def current_pos():
    #points are (top,25),(bottom,-25), (mpos,cdeg)
    #linear interpolation
    cdeg = 25 + ((convert_num(motor_lr.get_position()) - top)/(bottom - top)) * (-25 - 25)
    return cdeg

def convert_num(i):
    if (i <= 0):
        i = -180 + i
    else:
        i = 180 - i
    return i

if __name__ == "__main__":
    print("Calibrating")
    calibrate()
    straighten()
    print("Running Test\nStarting Forward thread")
    while(True):
        print(current_pos())
        time.sleep(0.5)
    #moveForward()
    #time.sleep(3)
    
    #turnLeft(30)
    #time.sleep(1)
    #turnRight(45)
    #time.sleep(5)
    #straighten()
    stop()
