#Menu Rgbled
#by Gauthier Defrance 11/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control

##---Périphériques---
from rgbled import *
from button import * #For creating Button object
from joystick import * #For creating Joystick object

def MenuRGBLed(MyScreen):
    """Load a Menu that allows to control the RGB led at pin 12."""
    ##---Joystick Presets---
    joystick = Joystick(26,27)
    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    ##---Leds Presets---
    rgb = RGBLed(12)
    r,g,b = 0,0,0
    rgb.quickColor(255,0,0)
    ##--- Setting Menu
    CaseR = Case(Point(200,0),80,80,"R",(254,254,254),(0,200,0),None)
    CaseG = Case(Point(200,81),80,80,"G",(254,254,254),(0,200,0),None)
    CaseB = Case(Point(200,162),80,80,"B",(254,254,254),(0,200,0),None)
    
    CaseRplus = Case(Point(281,0),80,80,"r+",(254,254,254),(0,200,0),None)
    CaseGplus = Case(Point(281,81),80,80,"g+",(254,254,254),(0,200,0),None)
    CaseBplus = Case(Point(281,162),80,80,"b+",(254,254,254),(0,200,0),None)
    
    CaseRmin = Case(Point(119,0),80,80,"-r",(254,254,254),(0,200,0),None)
    CaseGmin = Case(Point(119,81),80,80,"-g",(254,254,254),(0,200,0),None)
    CaseBmin = Case(Point(119,162),80,80,"-b",(254,254,254),(0,200,0),None)
    
    CaseBack = Case(Point(110,259),260,70,"Back",(254,254,254),(0,200,0),None)
    
    CaseR.setOffXY(10,10)
    CaseG.setOffXY(10,10)
    CaseB.setOffXY(10,10)
    CaseRplus.setOffXY(10,10)
    CaseGplus.setOffXY(10,10)
    CaseBplus.setOffXY(10,10)
    CaseRmin.setOffXY(10,10)
    CaseGmin.setOffXY(10,10)
    CaseBmin.setOffXY(10,10)
    
    CaseBack.setOffXY(60,40)
    
    ListLedRGBMenu = [[CaseRmin,CaseR,CaseRplus],
                       [CaseGmin,CaseG,CaseGplus],
                       [CaseBmin,CaseB,CaseBplus],
                       [CaseBack]]
    
    interfaceRGBLed = Interface(ListLedRGBMenu,"Setting")
    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceRGBLed.LoadInterface(MyScreen)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceRGBLed) 
        if ButtonR.read():
            if "r+" == interfaceRGBLed.getCurrentSelectedBox().getName():
                r=(r+10)%255
            elif "-r"==interfaceRGBLed.getCurrentSelectedBox().getName():
                r= (r-10)%255
            elif "g+"==interfaceRGBLed.getCurrentSelectedBox().getName():    
                g=(g+10)%255
            elif "-g"==interfaceRGBLed.getCurrentSelectedBox().getName():    
                g= (g-10)%255
            elif "b+"==interfaceRGBLed.getCurrentSelectedBox().getName():    
                b=(b+10)%255
            elif "-b"==interfaceRGBLed.getCurrentSelectedBox().getName():
                b= (b-10)%255
            elif "Back"==interfaceRGBLed.getCurrentSelectedBox().getName():
                loop=False
                
            print(r,g,b)
            rgb.quickColor(r,g,b)

        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    rgb.quickColor(0,0,0)
    interfaceRGBLed.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0