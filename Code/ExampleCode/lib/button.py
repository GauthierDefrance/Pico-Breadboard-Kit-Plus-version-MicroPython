#button by Gauthier Defrance 05/09/2024
from machine import Pin
#An optional class to understand with ease what pin is connected to what
#You can just use machine.Pin

class Button:
    def __init__(self,gp):
        """gp is for the gp pin where is connected your button."""
        self.pin = Pin(gp,Pin.IN, Pin.PULL_UP)
        
    def getpin(self):
        return self.pin
    
    def getgp(self):
        """Return the pin where the button point."""
        return self.gp
    
    def setgp(self,gp:int):
        """Change the pin where the button point."""
        self.gp = gp
        self.pin = Pin(gp,Pin.IN, Pin.PULL_UP)
        
    def read(self):
        """Function that return True if the button is pressed else it return False."""
        return not(self.pin())
    
    