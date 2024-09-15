#beeper by Gauthier Defrance 05/09/2024
from machine import Pin, PWM
from utime import sleep

#An optional class to understand with ease what pin is connected to what
#You can just use machine.Pin and machine.PWM

class Beeper:
    def __init__(self,gp):
        """gp is for the pin of the buzzer.
            You probably want to use : bequiet() to make the sound stop and beep() to play sounds."""
        self.gp = gp
        self.buzzer = PWM(Pin(self.gp))
        self.volume = 0
        self.buzzer.duty_u16(self.volume)
    
    def _setgp(self,gp):
        """Allow to change the pin where is connected the buzzer. Most of the time you don't want to change that."""
        self.gp = gp
        self.buzzer = PWM(Pin(self.gp))
    
    def getgp(self):
        """Return the pin of the buzzer."""
        return self.gp
    
    def bequiet(self):
        """This function will stop the buzzer. Don't be scared to use it."""
        self.buzzer.duty_u16(0)
    
    def Volume(self,volume:int):
        """Volume is for the intensity of the sounds that will come out of the buzzer. Please avoid using anything over 1000."""
        if volume>=0 and volume<=65535:
            self.volume = volume
            self.buzzer.duty_u16(self.volume)
        else:
            print(f"Volume can't be set to {volume}, it must be superior or equal to 0.")
        
    def beep(self,frequency:int,sleepTime:int):
        """Frequency is for the frequency of the sound, and sleepTime for the time the sound will be played before being shut"""
        if frequency>0:
            self.buzzer.duty_u16(self.volume)
            self.buzzer.freq(frequency)
        sleep(sleepTime)
        self.bequiet()
        
    def beepNoShut(self,frequency:int,sleepTime:int):
        """Frequency is for the frequency of the sound, and sleepTime for the time the sound will be played before leaving this program. The buzzer will continue to scream, it may be painfull. Please don't."""
        self.buzzer.duty_u16(self.volume)
        self.buzzer.freq(frequency)
        sleep(sleepTime)