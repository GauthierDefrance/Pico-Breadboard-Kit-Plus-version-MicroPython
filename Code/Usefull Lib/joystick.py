#joystick by Gauthier Defrance 05/09/2024
from machine import ADC,Pin

#An optional class to understand with ease what pin is connected to what
#You can just use machine.Pin and machine.ADC

class Joystick:
    def __init__(self,gpx,gpy):
        """gpx and gpy are for ADC pin.
        This class allow to easily control a joystick.
        You probably want to use getDirections() or for more precision getScanXY()."""
        self.gpx = gpx
        self.gpy = gpy
        self.XAxis = ADC(Pin(self.gpx))
        self.YAxis = ADC(Pin(self.gpy))

    def _setGPX(self,gpx):
        """Allow to change the pin where is connected the xAxis of the Joystick. Most of the time you don't want to change that."""
        self.gpx = gpx
        self.XAxis = ADC(Pin(self.gpx))
        
    def _setGPY(self,gpy):
        """Allow to change the pin where is connected the yAxis of the Joystick. Most of the time you don't want to change that."""
        self.gpy = gpy
        self.YAxis = ADC(Pin(self.gpy))
        
    def getGPX(self):
        """Return the pin where is connected the xAxis pin."""
        return self.gpx
        
    def getGPY(self):
        """Return the pin where is connected the yAxis pin."""
        return self.gpy
        
    def getScanXY(self):
        """Return the value of the xAxis and yAxis (divided by 1000) of the joystick."""
        return self.XAxis.read_u16()//1000,self.YAxis.read_u16()//1000
        
    def getDirections(self):
        """Return a tuple X,Y of two str. Each can take two value in normal scenario. 'Left' , 'Right' or 'Middle' and 'Up' , 'Down' or 'Middle'. Give the position of the Joystick."""
        return self.directionX(),self.directionY()
    
    def directionX(self):
        """Return 'Left' , 'Right' or 'Middle', depend on the position of the joystick."""
        x = self.scanX()
        if (x>=18 and x<=38):#Middle
            return "Middle"
        elif x<=18: #left
            return "Left"
        elif x>=38: #right
            return "Right"
        else:
            print(f"Something unexpected has happened, the value we scanned is : {x}./n You should see if your joystick is correctly set./n You can change the value of detection in the 'joystick' library.")
            return None
        
    def directionY(self):
        """Return 'Up' , 'Down' or 'Middle', depend on the position of the joystick."""
        y = self.scanY()
        if (46>=y and y>=26):#Middle
            return "Middle"
        elif y<=46: #Down
            return "Down"
        elif y>=26: #Up
            return "Up"
        else:
            print(f"Something unexpected has happened, the value we scanned is : {y}./n You should see if your joystick is correctly set./n You can change the value of detection in the 'joystick' library.")
            return None
        
    def scanX(self):
        """Return the value of the xAxis (divided by 1000) of the joystick. It should be beetween 3 and 61."""
        return self.XAxis.read_u16()//1000
        
    def scanY(self):
        """Return the value of the yAxis (divided by 1000) of the joystick. It should be beetween 5 and 63."""
        return self.YAxis.read_u16()//1000