#Piano
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control
from musicdata import NOTE_C4,NOTE_D4,NOTE_E4,NOTE_F4,NOTE_G4,NOTE_A4,NOTE_B4,NOTE_C5

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object
from beeper import * #For controlling the beeper

def MenuPiano(MyScreen):
    
    ##---Joystick Presets---
    joystick = Joystick(26,27)
    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    ##--- Beeper Presets ---
    beeper = Beeper(13) #Set the pin of the beeper
    beeper.Volume(1000) #Init the initial volume of the beeper
    beeper.bequiet() #Set that the beeper shall not make noise at the start.
    ##--- Setting Menu
    CaseC4 = Case(Point(0,1),59,100,"C4",(254,254,254),(0,200,0),None)
    CaseD4 = Case(Point(60,1),59,100,"D4",(254,254,254),(0,200,0),None)
    CaseE4 = Case(Point(120,1),59,100,"E4",(254,254,254),(0,200,0),None)
    CaseF4 = Case(Point(180,1),59,100,"F4",(254,254,254),(0,200,0),None)
    CaseG4 = Case(Point(240,1),59,100,"G4",(254,254,254),(0,200,0),None)
    CaseA4 = Case(Point(300,1),59,100,"A4",(254,254,254),(0,200,0),None)
    CaseB4 = Case(Point(360,1),59,100,"B4",(254,254,254),(0,200,0),None)
    CaseC5 = Case(Point(420,1),59,100,"C5",(254,254,254),(0,200,0),None)
    
    
    CaseBack = Case(Point(110,239),260,80,"Back",(254,254,254),(0,200,0),None)
    
    CaseC4.setOffXY(5,40)
    CaseD4.setOffXY(5,40)
    CaseE4.setOffXY(5,40)
    CaseF4.setOffXY(5,40)
    CaseG4.setOffXY(5,40)
    CaseA4.setOffXY(5,40)
    CaseB4.setOffXY(5,40)
    CaseC5.setOffXY(5,40)

    CaseBack.setOffXY(60,40)
    
    ListPianoMenu = [[CaseC4,CaseD4,CaseE4,CaseF4,CaseG4,CaseA4,CaseB4,CaseC5],
                       [CaseBack]]
    interfacePiano = Interface(ListPianoMenu,"Piano")
    MyScreen.Fill(MyScreen.color(0,0,0))
    interfacePiano.LoadInterface(MyScreen)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfacePiano) 
        if ButtonR.read():
            #Here we read wich touch of the virtual piano has been pressed
            #And if it's touch X we will play Y sound.
            if "C4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_C4,0.3)
            elif "D4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_D4,0.3)
            elif "E4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_E4,0.3)
            elif "F4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_F4,0.3)
            elif "G4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_G4,0.3)
            elif "A4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_A4,0.3)
            elif "B4" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_B4,0.3)
            elif "C5" == interfacePiano.getCurrentSelectedBox().getName():
                beeper.beep(NOTE_C5,0.3)
            elif "Back"==interfacePiano.getCurrentSelectedBox().getName():
                loop=False

        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    beeper.bequiet()
    interfacePiano.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0