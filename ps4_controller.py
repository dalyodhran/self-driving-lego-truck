from pyPS4Controller.controller import Controller

from motor import LegoMotor


class MyController(Controller):

    motor = LegoMotor()

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_share_press(self):
         print("Odhran_on_share_press")

    def on_options_press(self):
        print("Odhran_on_option_press")

    def on_L3_left(self, value):
        print('Turn Left')
        self.motor.turn_left(value)

    def on_L3_right(self, value):
        print('Turn Right')
        self.motor.turn_right(value)

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()