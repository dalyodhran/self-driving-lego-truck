from buildhat import Motor
import time

m = Motor('A')

while(True):
    print(m.get_aposition()," ",m.get_position())
    time.sleep(1)