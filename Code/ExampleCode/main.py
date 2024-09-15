
#Here all the usefulls Lib for the main Menu
##---Main Menu---
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
import os
from thready import* #Allow to easily to Threading (Warning, the raspberry pico only has one core !)
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from music import *
from control import Control

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object
from screen import * #For creating Screen object
import gc
import machine


##---Joystick Presets---
joystick = Joystick(26,27)

##---Button Presets---
ButtonL = Button(15)
ButtonR = Button(14)

##---Screen Presets---
sck=2
mosi=3
miso=4
cs=5
dc=6
reset=7
W=480 #width of the screen
H=320 #Heigth of the screen
#More options are avaible if needed.

##---Set Splash Screen ---
splash = "rpimg.rgb565"
splashWH = (102,126)
splashP = Point(480-splashWH[0],0)
splashText = ("Raspberry","Unofficial")
data = 'data.txt'

def SplashScreen(MyScreen):
    try:
        f = open(data)
        text = f.readlines()
        f.close()
        if text[0]=='SplashScreen = True':
            try:
                MyScreen.Text(Point(20,230),splashText[0],MyScreen.color(200,200,200),3)
                MyScreen.Text(Point(20,255),splashText[1],MyScreen.color(200,200,200),2)
                MyScreen.display_image(splash,splashWH[1],splashWH[0],splashP)
                sleep(0.5)
                MyScreen.Fill(MyScreen.color(0,0,0))
            except:
                print(f"File not found : {splash}")
        else:
            print("Splash screen set to False.")
    except:
        print(f"File not found : {data}")


##--- Main Menu ---
CasePlay = Case(Point(30,50),120,100,"play",(254,254,254),(0,200,0),None)
CaseMusic = Case(Point(180,50),120,100,"music",(254,254,254),(0,200,0),None)
CaseSettings = Case(Point(330,50),120,100,"setting",(254,254,254),(0,200,0),None)
CaseQuit = Case(Point(150,250),180,100,"Quit",(254,254,254),(0,200,0),None)

CasePlay.setOffXY(20,40)
CaseMusic.setOffXY(20,40)
CaseSettings.setOffXY(4,40)
CaseQuit.setOffXY(50,40)

ListMainMenu = [[CasePlay,
                 CaseMusic,
                 CaseSettings],
                [CaseQuit]
                ]

interfaceMain = Interface(ListMainMenu,"MainMenu")



##---Main program and menu
def Main():
    #First we will need to initialize a Screen object
    MyScreen = Screen(2,3,4,5,6,7,480,320)
    MyScreen.init()
    #Screen has been initialized
    
    MyScreen.Fill(MyScreen.color(20,20,20))
    SplashScreen(MyScreen) #Read if activated the Splash Screen
    interfaceMain.LoadInterface(MyScreen)
    s = os.statvfs('/')
    print(f"Free storage: {s[0]*s[3]/1024} KB")
    print(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
    print(f"CPU Freq: {machine.freq()/1000000}Mhz")
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceMain)
        if ButtonR.read():
            if "Quit"==interfaceMain.getCurrentSelectedBox().getName():
                loop=False
                
            elif "play"==interfaceMain.getCurrentSelectedBox().getName():
                import MenuPlay
                MenuPlay.MenuGame(MyScreen)
                del MenuPlay  # Libération de la mémoire après utilisation
                interfaceMain.reinit()
                interfaceMain.LoadInterface(MyScreen)
            
            elif "music"==interfaceMain.getCurrentSelectedBox().getName():
                import MenuMusic
                MenuMusic.MenuMusic(MyScreen)
                del MenuMusic  # Libération de la mémoire après utilisation
                interfaceMain.reinit()
                interfaceMain.LoadInterface(MyScreen)
                
                
            elif "setting"==interfaceMain.getCurrentSelectedBox().getName():
                import MenuSetting
                MenuSetting.MenuSetting(MyScreen)
                del MenuSetting  # Libération de la mémoire après utilisation
                interfaceMain.reinit()
                interfaceMain.LoadInterface(MyScreen)
                
        elif ButtonL.read():
            loop=False
        sleep(0.3)
        
    MyScreen.Fill(MyScreen.color(0,0,0))
    MyScreen.Sleep()
    return 0
        