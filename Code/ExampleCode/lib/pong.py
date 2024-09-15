#Pong by Gauthier Defrance 13/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.
from screen import *
##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control
from random import randint,uniform
from music import *
from thready import * #Thready will allow us to play music while playing the game.
from collisiondetector import Rectangle

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object
from beeper import *

def MenuPong(MyScreen):
    
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

    ListPlayPong = [[CasePlay],
                    [CaseBack]]

    interfaceGame = Interface(ListPlayPong,"MenuGame")

    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceGame.LoadInterface(MyScreen)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceGame) 
        if ButtonR.read():
            if "Quit"==interfaceGame.getCurrentSelectedBox().getName():
                loop=False
                
            elif "Play"==interfaceGame.getCurrentSelectedBox().getName():
                
                Pong(MyScreen)
                MyScreen.Fill(MyScreen.color(0,0,0))
                interfaceGame.LoadInterface(MyScreen)
            
        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    interfaceGame.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0


def ThreadBeep(beeper,frequency,thread):
    beeper.Volume(1000)
    beeper.beep(frequency,0.2)
    thread.killThread()



def Pong(MyScreen):
    MyScreen.Fill(MyScreen.color(0,0,0))
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    beeper= Beeper(13)
    thread = Thread(ThreadBeep,())
    thread.setArgs((beeper,980,thread))
    
    ball = Ball(MyScreen,Point(200,150),20,20,"red")
    
    p1 = Pad(MyScreen,Point(10,100),20,100,"red")
    p1.load()
    
    p2 = Pad(MyScreen,Point(450,100),20,100,"red")
    p2.load()
    
    ball.load()
    x=2
    y=2
    xt = randint(0,1)
    yt = randint(0,1)
    if xt:
        x=-x
    if yt:
        y=-y
        
    Scorep1=0
    Scorep2=0
    loop=True
    sleep(1)
    while loop:
        
        directionx,directiony=joystick.getDirections()
        #Système collision balle   
        if ball.collideWallH():
            y = -y
            
        if ball.collideWallV():
            if ball.point.x>240:
                Scorep1+=1
            else:
                Scorep2+=1
            if Scorep1 + Scorep2>=5:
                loop=False
            print(f"P1:{Scorep1} / P2:{Scorep2}")
            ball.unload()
            ball.setPoint(200,150)
            ball.load()
            x=2
            y=2
            xt = randint(0,1)
            yt = randint(0,1)
            if xt:
                x=-x
            if yt:
                y=-y
            sleep(1)
            #x= -x
        
        if ball.willCollideH(p1,x,y):
            thread.start()
            x=-x*uniform(1, 1.2)
            ball.unload()
            ball.setPoint(p1.point.x+p1.width+1,ball.point.y)
            ball.load()
        elif ball.willCollideV(p1,x,y):
            y=-y*uniform(1, 1.2)
            ball.unload()
            ball.setPoint(p1.point.x+p1.width+1,ball.point.y)
            ball.load()
        elif ball.willCollideH(p1,x,y) and ball.willCollideV(p1,x,y):
            y=-y*uniform(1, 1.2)
            x=-x*uniform(1, 1.2)
            ball.unload()
            ball.setPoint(p1.point.x+p1.width+1,ball.point.y)
            ball.load()
            
        if ball.willCollideH(p2,x,y):
            thread.start()
            x=-x*uniform(1, 1.2)
            ball.unload()
            ball.setPoint(p2.point.x-(ball.width+1),ball.point.y)
            ball.load()
        elif ball.willCollideV(p2,x,y):
            y=-y*uniform(1, 1.2)
            ball.unload()
            ball.setPoint(p2.point.x-ball.width-1,ball.point.y)
            ball.load()
        elif ball.willCollideH(p2,x,y) and ball.willCollideV(p2,x,y):
            y=-y*uniform(1, 1.2)
            x=-x*uniform(1, 1.2)
            ball.unload()
            ball.setPoint(p2.point.x-ball.width-1,ball.point.y)
            ball.load()
        #Fin système collision
        
        ball.SmartMove(x,y)
        
        if ButtonR.read() and not ButtonL.read() and (not p2.collideWallH() or p2.point.y<=120):
            p2.SmartMove(0,4)
        elif ButtonL.read() and not ButtonR.read() and (not p2.collideWallH() or p2.point.y>120):
            p2.SmartMove(0,-4)
        elif ButtonR.read() and ButtonL.read():
            loop = False
            
        if directiony=="Up" and (not p1.collideWallH() or p1.point.y<=120):
            p1.SmartMove(0,4)
        elif directiony=="Down" and (not p1.collideWallH() or p1.point.y>120):
            p1.SmartMove(0,-4)
    
    MyScreen.Fill(MyScreen.color(0,0,0))
    if Scorep1>Scorep2:
        text = "Victory of P1"
    elif Scorep1<Scorep2:
        text = "Victory of P2"
    else:
        text = "Draw ?!"
    thread.setArgs((beeper,100,thread))
    thread.start()
    MyScreen.Text(Point(10,0),"GAME OVER",MyScreen.color(128,128,128),4)
    MyScreen.Text(Point(10,50),f"score P1={Scorep1}",MyScreen.color(128,128,128),2)
    MyScreen.Text(Point(10,100),f"score P2={Scorep2}",MyScreen.color(128,128,128),2)
    MyScreen.Text(Point(10,130),text,MyScreen.color(196,196,196),4)
    
    sleep(5)
    MyScreen.Fill(MyScreen.color(0,0,0))            
    return 0

class Entity:
    def __init__(self,MyScreen, point:Point, width:int, heigth:int, color=(255,255,255)):
        self.MyScreen=MyScreen
        self.point=point
        self.width=width
        self.heigth=heigth
        self.color=color
        self.body = Rectangle(self.point,self.width,self.heigth)
        self.MaxX=470
        self.MaxY=310
        
    def setPoint(self,x,y) -> None:
        self.point = Point(x,y)
    def getPoint(self) -> Point:
        return self.point
    def getBody(self) -> Rectangle:
        return self.body
    def getWidth(self) -> int:
        return self.width
    def getHeigth(self) -> int:
        return self.heigth
    def getColor(self):
        return self.color
    
    def load(self) -> None:
         self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y))),self.width,self.heigth,self.MyScreen.color(255,255,255),True)
         
    def unload(self) -> None:
         self.MyScreen.Rectangle(Point(int(round(self.point.x))-1,int(round(self.point.y))-1),self.width+2,self.heigth+2,self.MyScreen.color(0,0,0),True)
         
    def collide(self,other) -> bool:
        return self.body in other.body or other.body in self.body
    
    def willCollideH(self,other,x,y) -> bool:
        Fbody = Rectangle(self.point+Point(x,0),self.width,self.heigth)
        return Fbody in other.body or other.body in Fbody
    
    def willCollideV(self,other,x,y) -> bool:
        Fbody = Rectangle(self.point+Point(0,y),self.width,self.heigth)
        return Fbody in other.body or other.body in Fbody
    
    
    def collideWallH(self) -> bool:
        return  self.point.y<10 or self.point.y+self.heigth>self.MaxY
    
    def collideWallV(self) -> bool:    
        return self.point.x<10 or self.point.x+self.width>self.MaxX
    
    def move(self,x:int,y:int):
        self.point += Point(x,y)
        self.body = Rectangle(self.point,self.width,self.heigth)
        
    
class Ball(Entity):
    def __init__(self,MyScreen, point, width, heigth, color):
        super().__init__(MyScreen, point, width, heigth, color)
        self.Speedx = 0
        self.Speedy = 0
        
    
    def SmartMove(self,x:int,y:int):
        P2 = self.point+Point(x,y)
        self.MyScreen.Rectangle(Point(int(round(P2.x)),int(round(P2.y))),self.width,self.heigth,self.MyScreen.color(255,255,255),True)
        
        if x>0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y))),int(round(abs(x)))+1,self.heigth,self.MyScreen.color(0,0,0),True)
            
        elif x<0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y)))+Point(int(round(self.width+x)),0),int(abs(round(x)))+1,self.heigth,self.MyScreen.color(0,0,0),True)
        
        if y >0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y))),self.width,1+int(round(abs(y))),self.MyScreen.color(0,0,0),True)
        elif y<0:
            self.MyScreen.Rectangle(Point(int(round(self.point.x)),int(round(self.point.y)))+Point(0,int(round(self.heigth+y))),self.width,1+int(round(abs(y))),self.MyScreen.color(0,0,0),True)
        
        self.point = P2
        self.body = Rectangle(self.point,self.width,self.heigth)
        
        
    def isOut(self) -> bool:
        return self.point.x<0 or self.point.x+self.width>480
        
class Pad(Entity,Ball):
    def __init__(self,MyScreen, point, width, heigth, color):
        super().__init__(MyScreen, point, width, heigth, color)

    
    

    
    
    