#MenuMusic by Gauthier Defrance 15/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
from thready import* #Allow to easily to Threading (Warning, the raspberry pico only has one core !)
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from music import *
from control import Control

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object
from beeper import *



def MenuMusic(MyScreen):
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    ##--- Beeper ---
    beeper = Beeper(13)
    beeper.bequiet()
    
    ##--- Music Menu
    CaseLastMusic = Case(Point(115,269),50,50,"<||",(254,254,254),(0,200,0),None)
    CaseNextMusic = Case(Point(315,269),50,50,"||>",(254,254,254),(0,200,0),None)
    CasePlay = Case(Point(190,219),100,100,"|>",(254,254,254),(0,200,0),None)
    CaseVolumeMore = Case(Point(0,269),50,50,"+",(254,254,254),(0,200,0),None)
    CaseVolumeLess = Case(Point(51,269),50,50,"-",(254,254,254),(0,200,0),None)
    CaseMusicName  = Case(Point(90,1),300,100,"Current Music",(254,254,254),(0,200,0),None)
    CaseBackMusic = Case(Point(400,269),80,50,"Back",(254,254,254),(0,200,0),None)

    CaseLastMusic.setOffXY(2,15)
    CaseNextMusic.setOffXY(2,15)
    CasePlay.setOffXY(20,40)
    CaseVolumeMore.setOffXY(5,15)
    CaseVolumeLess.setOffXY(5,15)
    CaseMusicName.setOffXY(20,40)
    CaseBackMusic.setOffXY(10,15)

    ListMusicMenu = [[CaseMusicName],
                    [CaseVolumeMore,CaseVolumeLess,CaseLastMusic,CasePlay,CaseNextMusic,CaseBackMusic]]

    interfaceMusic = Interface(ListMusicMenu,"Setting")
    
    MusicList = [SuperMariosBros,Rick,ChristmasMusic,TetrisMusic,GodFatherMusic,imperialmarch,StarWars,CantinaBand,
                 PinkPanther,OdeToJoy,PacMan,Doom,HappyBirthday,KeyBoardCat,MiiMusic,GameOfthrones]
    MusicTempo = [256,256,256,256,256,256,256,600,
                  256,256,512,512,256,256,256,256]
    MusicSelector = 0
    
    
    
    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceMusic.LoadInterface(MyScreen)
    loop = True
    
    music=Music(512,beeper)
    music.Loop(True)
    music.Volume(1000)
    music.Continue()
    
    beeper.bequiet()
    thread = Thread(ThreadMusic,())
    thread.setArgs((music,thread,MusicList[MusicSelector]))
    CaseMusicName.setName(str(MusicList[MusicSelector].__name__))
    MyScreen.Rectangle(CaseMusicName.PointA,CaseMusicName.width,CaseMusicName.heigth,MyScreen.color(0,0,0),True)
    while loop:
        Control(MyScreen,joystick,interfaceMusic) 
        if ButtonR.read():
            if "Back"==interfaceMusic.getCurrentSelectedBox().getName():
                loop=False
                
            elif "|>"==interfaceMusic.getCurrentSelectedBox().getName():
                if not music.isPlaying():
                    thread = Thread(ThreadMusic,())
                    music.setTempo(MusicTempo[MusicSelector])
                    thread.setArgs((music,thread,MusicList[MusicSelector]))
                    thread.start()
                
                if not(music.isPaused()) and music.isPlaying():
                    music.pause = True
                    
                elif (music.isPaused() and music.isPlaying()):
                    music.pause = False
            
            elif "||>"==interfaceMusic.getCurrentSelectedBox().getName():
                music.Stop()
                sleep(1)
                MusicSelector = (MusicSelector+1)%len(MusicList)
                CaseMusicName.setName(str(MusicList[MusicSelector].__name__))
                MyScreen.Rectangle(CaseMusicName.PointA,CaseMusicName.width,CaseMusicName.heigth,MyScreen.color(0,0,0),True)
                music.Continue()
                music.play = True
                thread = Thread(ThreadMusic,())
                music.setTempo(MusicTempo[MusicSelector])
                thread.setArgs((music,thread,MusicList[MusicSelector]))
                thread.start()
                interfaceMusic.LoadInterface(MyScreen)
            elif "<||"==interfaceMusic.getCurrentSelectedBox().getName():
                music.Stop()
                sleep(1)
                MusicSelector = (MusicSelector-1)%len(MusicList)
                CaseMusicName.setName(str(MusicList[MusicSelector].__name__))
                MyScreen.Rectangle(CaseMusicName.PointA,CaseMusicName.width,CaseMusicName.heigth,MyScreen.color(0,0,0),True)
                music.Continue()
                music.play = True
                thread = Thread(ThreadMusic,())
                music.setTempo(MusicTempo[MusicSelector])
                thread.setArgs((music,thread,MusicList[MusicSelector]))
                thread.start()
                interfaceMusic.LoadInterface(MyScreen)
            elif "+"==interfaceMusic.getCurrentSelectedBox().getName():
                if (music.getVolume()+100)<60000:
                    music.Volume((music.getVolume()+100))
            
            elif "-"==interfaceMusic.getCurrentSelectedBox().getName():
                if (music.getVolume()-100)>0:
                    music.Volume((music.getVolume()-100))
                elif (music.getVolume()-100)<0:
                    music.Volume(0)
            
        elif ButtonL.read():
            loop=False
            
        sleep(0.3)
    music.Stop()
    interfaceMusic.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0

def ThreadMusic(music,thread,name):
    music.Volume(1000)
    music.Play(name())
    thread.killThread()
