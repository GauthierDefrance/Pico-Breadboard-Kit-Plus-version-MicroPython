#Space invaders by Gauthier Defrance 15/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.
from screen import *
##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control
from random import randint,uniform
from music import Music
from musicdata import Doom
from thready import * #Thready will allow us to play music while playing the game.
from collisiondetector import Rectangle
from random import randint

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object
from beeper import *
import gc 


def MenuSpaceInvaders(MyScreen):
    gc.collect()
    MyScreen.Fill(MyScreen.color(0,0,0))
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    
    
    ##---Play Menu ---
    CasePlay = Case(Point(140,50),200,100,"Play",(254,254,254),(0,200,0),None)
    CaseBack = Case(Point(140,151),200,100,"Quit",(254,254,254),(0,200,0),None)
    CasePlay.setOffXY(50,40)
    CaseBack.setOffXY(50,40)

    ListPlaySpaceInvaders = [[CasePlay],
                    [CaseBack]]

    interfaceGame = Interface(ListPlaySpaceInvaders,"MenuGame")

    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceGame.LoadInterface(MyScreen)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceGame) 
        if ButtonR.read():
            if "Quit"==interfaceGame.getCurrentSelectedBox().getName():
                loop=False
                
            elif "Play"==interfaceGame.getCurrentSelectedBox().getName(): 
                SpaceInvaders(MyScreen)
                MyScreen.Fill(MyScreen.color(0,0,0))
                interfaceGame.LoadInterface(MyScreen)
            
        elif ButtonL.read():
            loop=False
        
        sleep(0.3)
    
    interfaceGame.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0


def ThreadMusic(music,thread):
    music.Volume(1000)
    music.Play(Doom())
    thread.killThread()



def SpaceInvaders(MyScreen):
    MyScreen.Fill(MyScreen.color(0,0,0))
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    Player = Entity(MyScreen,Point(230,300),20,20,"Player",MyScreen.color(0,255,0))
    
    beeper= Beeper(13)
    music = Music(512,beeper)
    music.Loop(True)
    thread = Thread(ThreadMusic,())
    thread.setArgs((music,thread))
    thread.start()
    
    playerspeed=10
    speed = 10
    AlienList = [[Entity(MyScreen,Point(10+Y*10+X*40,40*Y),20,20,"Alien",MyScreen.color(255,255,196),(speed)*((-1)**Y)) for X in range(11)] for Y in range(2)]
    BulletList = []
    for elem in AlienList:
        for elemP in elem:
            elemP.load()
    playzone = Rectangle(Point(0,0),480,320)
    
    Player.load()
    win = False
    loop = True
    shoottime=0
    while loop==True:
        gc.collect()
        directionx,directiony=joystick.getDirections()
        #This parts moves the alien.
        AlienMove(AlienList,BulletList,playzone,MyScreen)
        BulletMove(BulletList,playzone,MyScreen)
        contact(Player,BulletList,AlienList,MyScreen)
        for Y in range(len(AlienList)):
            for X in range(len(AlienList[Y])):
                try:
                    
                    if not AlienList[Y][X].getAlive():
                        AlienList[Y].remove(AlienList[Y][X])
                        
                except:
                    pass
        
        if directionx=="Right" and ((not Player.collideWallV())or Player.point.x+Player.width<Player.MaxX):
            Player.SmartMove((1)*playerspeed,0)
        elif directionx=="Left" and ((not Player.collideWallV())or Player.point.x>0):
            Player.SmartMove((-1)*playerspeed,0)
        
        if ButtonR.read() and shoottime > 5:
            shoot(BulletList,Player,MyScreen)
            shoottime=0
            
        elif ButtonL.read():
            loop = False

        
        if not Player.getAlive():
            loop=False
        
        if AlienList==[[],[]]:
            win = True
            loop=False
        shoottime+=1
        sleep(0.1)
    
    music.Stop()
    MyScreen.Fill(MyScreen.color(0,0,0))
    text ="Defeat"
    text2 = "The earth has been conquered."
    if win:text,text2="Victory !","May the earth live another day."
    MyScreen.Text(Point(10,0),"GAME OVER",MyScreen.color(128,128,128),4)
    MyScreen.Text(Point(10,50),f"{text}",MyScreen.color(128,128,128),2)
    MyScreen.Text(Point(0,100),f"{text2}",MyScreen.color(128,128,128),2)
    sleep(4)
    MyScreen.Fill(MyScreen.color(0,0,0))            
    return 0


def contact(Player,BulletList,AlienList,MyScreen):
    for bullet in BulletList:
        for elem in AlienList:
            i=0
            for elemP in elem:
                if bullet.Name=="BulletPlayer" and bullet.body in elemP.body:
                    bullet.setAlive(False)
                    elemP.unload()
                    elemP.setAlive(False)
                elif elemP.body in Player.body:
                    Player.setAlive(False)
                i+=1
        if bullet.Name=="BulletAlien" and bullet.body in Player.body:
            bullet.setAlive(False)
            Player.setAlive(False)
        if bullet.isOutY():
            bullet.setAlive(False)
            
    for bullet1 in BulletList:
        if bullet1.point.y<0 or bullet1.point.y>320:
            bullet1.setAlive(False)
        else:
            for bullet2 in BulletList:
                if bullet1!=bullet2 and bullet1.body in bullet2.body and bullet1.getName()!=bullet2.getName():
                    bullet1.setAlive(False)
                    bullet2.setAlive(False)
                
def shoot(BulletList,shooter,MyScreen):
    width = 5
    heigth = 15
    if shooter.Name == "Alien":
        BulletList.append(Entity(MyScreen,Point(shooter.width//2+shooter.point.x,shooter.point.y+shooter.heigth+10),width,heigth,"BulletAlien",MyScreen.color(255,0,0),0,5))
    elif shooter.Name == "Player":
        BulletList.append(Entity(MyScreen,Point(shooter.width//2+shooter.point.x,shooter.point.y-heigth),width,heigth,"BulletPlayer",MyScreen.color(255,0,255),0,-10))
            
def BulletMove(BulletList,playzone,MyScreen):
    for elem in BulletList:
                if (elem.point.y>-10 and elem.point.y<340) and elem.getAlive():
                    elem.SmartMove(0,elem.directiony)
                elif not(elem.getAlive()) or elem.isOutY():
                    elem.unload()
                    BulletList.remove(elem)
                elif not((elem.point.y>-10 and elem.point.y<340)):
                    elem.unload()
                    try:
                        BulletList.removeAlienMove(AlienList,BulletList,playzone)(elem)
                    except:
                        pass
def AlienMove(AlienList,BulletList,playzone,MyScreen):
    for elem in AlienList:
            for elemP in elem:
                if (elemP.body in playzone) and elemP.getAlive():
                    if elemP.collideWallV():
                        elemP.directionx=elemP.directionx*(-1)
                        elemP.unload()
                        elemP.setPoint(elemP.getPoint().x,elemP.getPoint().y+40)
                        elemP.load()
                    elemP.SmartMove(elemP.directionx,0)
                elif elemP.getAlive():
                    elemP.unload()
                    elemP.setAlive(False)
                if randint(0,4+len(elem)**2)==1:
                            shoot(BulletList,elemP,MyScreen)

class Entity:
    def __init__(self,MyScreen, point:Point, width:int, heigth:int,Name, color=(255,255,255),directionx=0,directiony=0):
        self.MyScreen=MyScreen
        self.point=point
        self.width=width
        self.heigth=heigth
        self.color=color
        self.body = Rectangle(self.point,self.width,self.heigth)
        self.MaxX=470
        self.MaxY=310
        self.Name = Name
        self.directionx = directionx
        self.directiony = directiony
        self.alive = True
    
    def getAlive(self):
        return self.alive
    def setAlive(self,alive):
        self.alive = alive
    
    def getName(self):
        return self.Name
    def getdirectionXY(self):
        return self.directionx,self.directiony
    def setdirectionXY(self,x,y):
        self.directionx,self.directiony = x,y
    def setPoint(self,x,y):
        self.point = Point(x,y)
    def getPoint(self):
        return self.point
    def getBody(self):
        return self.body
    def getWidth(self):
        return self.width
    def getHeigth(self):
        return self.heigth
    def getColor(self):
        return self.color
    
    def load(self):
         self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y))),self.width,self.heigth,self.color,True)
         
    def unload(self):
         self.MyScreen.Rectangle(Point(int(round(self.point.x))-1,int(round(self.point.y))-1),self.width+2,self.heigth+2,self.MyScreen.color(0,0,0),True)
         
    def collide(self,other):
        return self.body in other.body or other.body in self.body
    
    def willCollideH(self,other,x,y):
        Fbody = Rectangle(self.point+Point(x,0),self.width,self.heigth)
        return Fbody in other.body or other.body in Fbody
    
    def willCollideV(self,other,x,y):
        Fbody = Rectangle(self.point+Point(0,y),self.width,self.heigth)
        return Fbody in other.body or other.body in Fbody
    
    
    def collideWallH(self):
        return  self.point.y<10 or self.point.y+self.heigth>self.MaxY
    
    def collideWallV(self):    
        return self.point.x<10 or self.point.x+self.width>self.MaxX
    
    def move(self,x,y):
        self.point += Point(x,y)
        self.body = Rectangle(self.point,self.width,self.heigth)
        
    def SmartMove(self,x,y):
        P2 = self.point+Point(x,y)
        self.MyScreen.Rectangle(Point(int(round(P2.x)),int(round(P2.y))),self.width,self.heigth,self.color,True)
        
        if x>0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y))),int(round(abs(x)))+1,self.heigth,self.MyScreen.color(0,0,0),True)
            
        elif x<0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y)))+Point(int(round(self.width+x)),0),int(abs(round(x)))+1,self.heigth,self.MyScreen.color(0,0,0),True)
        
        if y >0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y))),self.width,1+int(round(abs(y))),self.MyScreen.color(0,0,0),True)
        elif y<0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y)))+Point(0,int(round(self.heigth+y))),self.width,int(round(abs(y))),self.MyScreen.color(0,0,0),True)
        
        self.point = P2
        self.body = Rectangle(self.point,self.width,self.heigth)    

    def isOutY(self):
        return self.point.y+self.heigth<0 or self.point.y>480
    def isOutX(self):
        return self.point.x<0 or self.point.x+self.width>480
        
        
#-------------
NOTE_B0 = 31
NOTE_C1=  33
NOTE_CS1= 35
NOTE_D1 = 37
NOTE_DS1 =39
NOTE_E1  =41
NOTE_F1  =44
NOTE_FS1 =46
NOTE_G1  =49
NOTE_GS1 =52
NOTE_A1  =55
NOTE_AS1 =58
NOTE_B1  =62
NOTE_C2  =65
NOTE_CS2 =69
NOTE_D2  =73
NOTE_DS2 =78
NOTE_E2  =82
NOTE_F2  =87
NOTE_FS2 =93
NOTE_G2  =98
NOTE_GS2 =104
NOTE_A2  =110
NOTE_AS2 =117
NOTE_B2  =123
NOTE_C3  =131
NOTE_CS3 =139
NOTE_D3  =147
NOTE_DS3 =156
NOTE_E3  =165
NOTE_F3  =175
NOTE_FS3 =185
NOTE_G3  =196
NOTE_GS3 =208
NOTE_A3  =220
NOTE_AS3 =233
NOTE_B3  =247
NOTE_C4  =262
NOTE_CS4 =277
NOTE_D4  =294
NOTE_DS4 =311
NOTE_E4  =330
NOTE_F4  =349
NOTE_FS4 =370
NOTE_G4  =392
NOTE_GS4 =415
NOTE_A4  =440
NOTE_AS4 =466
NOTE_B4  =494
NOTE_C5  =523
NOTE_CS5 =554
NOTE_D5  =587
NOTE_DS5 =622
NOTE_E5  =659
NOTE_F5  =698
NOTE_FS5 =740
NOTE_G5  =784
NOTE_GS5 =831
NOTE_A5  =880
NOTE_AS5 =932
NOTE_B5  =988
NOTE_C6  =1047
NOTE_CS6 =1109
NOTE_D6  =1175
NOTE_DS6 =1245
NOTE_E6  =1319
NOTE_F6  =1397
NOTE_FS6 =1480
NOTE_G6  =1568
NOTE_GS6 =1661
NOTE_A6  =1760
NOTE_AS6 =1865
NOTE_B6  =1976
NOTE_C7  =2093
NOTE_CS7 =2217
NOTE_D7  =2349
NOTE_DS7 =2489
NOTE_E7  =2637
NOTE_F7  =2794
NOTE_FS7 =2960
NOTE_G7  =3136
NOTE_GS7 =3322
NOTE_A7  =3520
NOTE_AS7 =3729
NOTE_B7  =3951
NOTE_C8  =4186
NOTE_CS8 =4435
NOTE_D8  =4699
NOTE_DS8 =4978
REST =0
#------------    



