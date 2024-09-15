#MenuSetting
#by Gauthier Defrance 10/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control
from MenuLed import *
from MenuLedRGB import *

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object


def MenuSetting(MyScreen):
    """Load a menu that allows to turn on and off the splash screen and access the Led Menu and RGB led menu."""
    data = 'data.txt'
    ##---Joystick Presets---
    joystick = Joystick(26,27)
    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    ##--- Setting Menu
    CaseLed = Case(Point(0,0),160,100,"Led",(254,254,254),(0,200,0),None)
    CaseRGBled = Case(Point(161,0),158,100,"RGB led",(254,254,254),(0,200,0),None)
    CaseSplashScreen = Case(Point(320,0),160,100,"Splash",(254,254,254),(0,200,0),None)
    CaseBack = Case(Point(160,250),160,100,"Back",(254,254,254),(0,200,0),None)
    
    CaseLed.setOffXY(20,40)
    CaseRGBled.setOffXY(20,40)
    CaseSplashScreen.setOffXY(20,40)
    CaseBack.setOffXY(20,40)
    
    ListSettingMenu = [[CaseLed,CaseRGBled,CaseSplashScreen],
                    [CaseBack]]
    interfaceSetting = Interface(ListSettingMenu,"Setting")
    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceSetting.LoadInterface(MyScreen)
    loop = True
    f = open(data)
    text = f.readlines()
    f.close()
    if text[0]=='SplashScreen = True':
        MyScreen.Rectangle(Point(320,101),160,20,MyScreen.color(0,255,0),True)
    else :
        MyScreen.Rectangle(Point(320,101),160,20,MyScreen.color(255,0,0),True)
    while loop:
        Control(MyScreen,joystick,interfaceSetting) 
        if ButtonR.read():
            if "Back"==interfaceSetting.getCurrentSelectedBox().getName():
                loop=False
                
            elif "Led"==interfaceSetting.getCurrentSelectedBox().getName():
                MenuLed(MyScreen) 
                interfaceSetting.reinit()
                interfaceSetting.LoadInterface(MyScreen)
                
            elif "RGB led"==interfaceSetting.getCurrentSelectedBox().getName():
                MenuRGBLed(MyScreen)
                interfaceSetting.reinit()
                interfaceSetting.LoadInterface(MyScreen)
            
            elif "Splash"==interfaceSetting.getCurrentSelectedBox().getName():
                try:
                    f = open(data)
                    text = f.readlines()
                    f.close()
                    if text[0]=='SplashScreen = True':
                        f = open(data, "w")
                        f.write('SplashScreen = False')
                        f.close()
                        MyScreen.Rectangle(Point(320,101),160,20,MyScreen.color(255,0,0),True)
                    elif text[0]=='SplashScreen = False':
                        f = open(data, "w")
                        f.write('SplashScreen = True')
                        f.close()
                        MyScreen.Rectangle(Point(320,101),160,20,MyScreen.color(0,255,0),True)
                except:
                    print("Something went wrong")
                    
                    
        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    interfaceSetting.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0


