#Menu led
#by Gauthier Defrance 10/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control

##---Périphériques---
from led import *
from button import * #For creating Button object
from joystick import * #For creating Joystick object

def MenuLed(MyScreen):
    """Load a menu that allows to control the leds at pin 16,17 and on board."""
    ##---Joystick Presets---
    joystick = Joystick(26,27)
    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    ##---Leds Presets---
    ledBoard,ledBoardState = Led('LED'),False
    led16,led16State = Led(16),False
    led17,led17State = Led(17),False
    
    ##--- Setting Menu
    CaseLed16 = Case(Point(110,0),260,79,"Led 16",(254,254,254),(0,200,0),None)
    CaseLed17 = Case(Point(110,80),260,79,"Led 17",(254,254,254),(0,200,0),None)
    CaseLED = Case(Point(110,160),260,79,"Board Led",(254,254,254),(0,200,0),None)
    CaseBack = Case(Point(110,239),260,80,"Back",(254,254,254),(0,200,0),None)
    
    CaseLED.setOffXY(5,40)
    CaseLed16.setOffXY(5,40)
    CaseLed17.setOffXY(5,40)
    CaseBack.setOffXY(60,40)
    
    ListLedMenu = [[CaseLed16],
                       [CaseLed17],
                       [CaseLED],
                       [CaseBack]]
    interfaceLed = Interface(ListLedMenu,"Setting")
    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceLed.LoadInterface(MyScreen)
    MyScreen.Rectangle(Point(370,0),20,80,MyScreen.color(255,0,0),True)
    MyScreen.Rectangle(Point(370,80),20,80,MyScreen.color(255,0,0),True)
    MyScreen.Rectangle(Point(370,160),20,80,MyScreen.color(255,0,0),True)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceLed) 
        if ButtonR.read():
            if "Led 16" == interfaceLed.getCurrentSelectedBox().getName():
                if led16State:
                    led16State=False
                    led16.off()
                    MyScreen.Rectangle(Point(370,0),20,80,MyScreen.color(255,0,0),True)
                else:
                    led16State=True
                    led16.on()
                    MyScreen.Rectangle(Point(370,0),20,80,MyScreen.color(0,255,0),True)


            elif "Led 17" == interfaceLed.getCurrentSelectedBox().getName():
                if led17State:
                    led17State=False
                    led17.off()
                    MyScreen.Rectangle(Point(370,80),20,80,MyScreen.color(255,0,0),True)
                else:
                    led17State=True
                    led17.on()
                    MyScreen.Rectangle(Point(370,80),20,80,MyScreen.color(0,255,0),True)

            elif "Board Led" == interfaceLed.getCurrentSelectedBox().getName():
                if ledBoardState:
                    ledBoardState=False
                    ledBoard.off()
                    MyScreen.Rectangle(Point(370,160),20,80,MyScreen.color(255,0,0),True)
                else:
                    ledBoardState=True
                    ledBoard.on()
                    MyScreen.Rectangle(Point(370,160),20,80,MyScreen.color(0,255,0),True)
                    
            elif "Back"==interfaceLed.getCurrentSelectedBox().getName():
                loop=False

        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    led16.off()
    led17.off()
    ledBoard.off()
    interfaceLed.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0