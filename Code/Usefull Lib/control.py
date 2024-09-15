from joystick import *
from screen import *
from interface import *

def Control(MyScreen,joystick,interface):
    x,y = joystick.getDirections()
    if y=="Up":
        interface.nextY(-1)
        interface.LoadInterface(MyScreen)
    elif y=="Down":
        interface.nextY(1)
        interface.LoadInterface(MyScreen)
    elif x == "Right":
        interface.nextX(1)
        interface.LoadInterface(MyScreen)
    elif x == "Left":
        interface.nextX(-1)
        interface.LoadInterface(MyScreen)