from joystick import *
from screen import *
from interface import *

def Control(MyScreen,joystick,interface):
    """A simple function, take an interface List, a joystick object and a Screen.
    If the joystick goes up,down,right or left. It will automatically change 
    the currently selected box."""
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