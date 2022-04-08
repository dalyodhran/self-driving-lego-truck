from pyPS4Controller.controller import Controller
from motor import turnLeft


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_share_press(self):
         print("Odhran_on_share_press")

    def on_options_press(self):
        print("Odhran_on_option_press")

    def on_L3_left(self, value):
        print(value)

    def on_L3_right(self, value):
        print(value)

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()