#RGBLeds by Gauthier Defrance 06/09/2024
from neopixel2 import Neopixel

#An optional class to understand with ease what pin is connected to what
#You can just use neopixel

class RGBLed:
    def __init__(self,gp,brightness=10):
        """gp is for where is the RGB led pin connected, you have the optional argument brightness set at 10%."""
        #10 is the default value for brightness, over that it will cook your eyes. Can go from 1 to 100.
        self.gp = gp
        self.brightness = brightness
        self.pixel = Neopixel(1, 0, self.gp, "RGB")
        self.pixel.brightness(self.brightness)
        #1 is because there is only one RGB led on the board model : WS2812
        #0 is for the current state of the machine
        #gp is for the pin of where is it connected
        #"RGB" is there to select beetween "RGB" mode or "RGBW". Only "RGB" works.
        
    def _setluminosity(self,x):
        """Increase or decrease the luminosity of the RGB led. Can go from 1 to 100. Warning the led can become too bright for your eyes."""
        self.brightness = x
        self.pixel.brightness(self.brightness)
        
    def _setgp(self,gp):
        """Allow to change the pin where is connected the RGB led. Most of the time you don't want to change that."""
        self.gp = gp
        self.pixel = Neopixel(1, 0, self.gp, "RGB")
    
    def getgp(self):
        """Return the pin of the RGB led."""
        return self.gp
    
    def setColor(self,r,g,b):
        """Change the future color of the led, but it won't show."""
        self.pixel.set_pixel(0, (g, r, b))
        
    def getColor(self):
        """Return the current color of the led."""
        return self.pixel.get_pixel(self.gp)
    
    def show(self):
        """Actualize the led, if you used setColor and then this function. It will change the color of the led."""
        self.pixel.show()
        
    def quickColor(self,r,g,b):
        """Change the current color and show it"""
        self.setColor(r,g,b)
        self.show()
        
    def stop(self):
        """Renitialize to (0,0,0) the led."""
        self.pixel.clear()
        