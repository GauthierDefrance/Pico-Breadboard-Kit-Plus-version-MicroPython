#Led by Gauthier Defrance 05/09/2024
from machine import Pin
from utime import sleep
#An optional class to understand with ease what pin is connected to what
#You can just use machine.Pin


class Led:
    def __init__(self,gp):
        """gp is for the pin of the led. write 'LED' instead to use the onboard led.
        You probably want to mainly use the toggle() function."""
        self.gp = gp
        self.led = Pin(gp, Pin.OUT)
        self.blinktime = 0.25
    
    def _setblinktime(self,blinktime):
        """Allow to change the timing beetween each blink.
            Per default it is 0.25 seconds. """
        self.blinktime = blinktime
        
        
    def getblinktime(self):
        """Return the current blinkTime."""
        return self.blinktime
    
    def _setgp(self,gp):
        """Allow to change the pin where is connected the led. Most of the time you don't want to change that."""
        self.gp = gp
        self.led = Pin(gp, Pin.OUT)
        
    def getgp(self):
        """Return the pin of the led."""
        return self.gp
    
    def blink(self,n):
        """Turn the led on and off n times.
            Blocking instruction, you will have to wait 2n*blinktime seconds."""
        for _ in range(n):
            self.toggle()
            sleep(self.blinktime)
            self.toggle()
            sleep(self.blinktime)
            
    def toggle(self):
        """Turn the led on and off depending of it's state."""
        self.led.toggle()
    
    def off(self):
        """Try to turn the led off for sure."""
        self.led.value(0)
        
    def on(self):
        """Try to turn the led on for sure."""
        self.led.value(1)