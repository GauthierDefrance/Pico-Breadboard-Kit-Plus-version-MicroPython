#snake by Gauthier Defrance 12/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.
from screen import *
##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control
from random import randint
from music import *
from thready import * #Thready will allow us to play music while playing the game.

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object
from beeper import *

###### Informations ######
# L'écran mesure 480x320 pixels
# Nous allons donc découper l'écran en pleins de petites cases pour que notre serpents puisse se déplacer
# On dira que une case = 32 pixels, soit on découpera l'écran en 15x10 cases 15x32 = 480 et 10x32=320.


def MenuSnake(MyScreen):
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    red = (255,0,0)
    green = (200,10,10)
    blue = (0,0,255)
    yellow = (255,255,0)
    purple = (128,0,128)
    silver = (192,192,192)
    aqua = (0,255,255)
    
    colorList = [red,green,blue,yellow,purple,silver,aqua]
    colorListSelector = 0
    NbFruits =2
    ##---Play Menu ---
    CasePlay = Case(Point(60,0),200,100,"Play",(254,254,254),(0,200,0),None)
    CaseColor = Case(Point(261,0),200,100,"Color",(254,254,254),(0,200,0),None)
    CaseNbFruits = Case(Point(60,101),200,100,f"Nb fruits {NbFruits}",(254,254,254),(0,200,0),None)
    CaseWallKill = Case(Point(261,101),200,100,"WallKill",(254,254,254),(0,200,0),None)
    CaseBack = Case(Point(190,240),200,80,"Quit",(254,254,254),(0,200,0),None)
    
    
    
    CasePlay.setOffXY(50,40)
    CaseColor.setOffXY(50,40)
    CaseNbFruits.setOffXY(50,40)
    CaseNbFruits.setOffXY(1,40)
    CaseWallKill.setOffXY(50,40)
    CaseBack.setOffXY(50,40)

    ListPlaySnake = [[CasePlay,CaseColor],
                      [CaseNbFruits,CaseWallKill],
                      [CaseBack]]

    interfaceGame = Interface(ListPlaySnake,"MenuGame")
    CaseColor.color = colorList[colorListSelector]
    CaseWallKill.color = (255,0,0)
    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceGame.LoadInterface(MyScreen)
    
    WallKill=False
    
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceGame) 
        if ButtonR.read():
            if "Quit"==interfaceGame.getCurrentSelectedBox().getName():
                loop=False
            elif "Color"==interfaceGame.getCurrentSelectedBox().getName():
                colorListSelector = (colorListSelector+1)%len(colorList)
                interfaceGame.getCurrentSelectedBox().color = colorList[colorListSelector]
                interfaceGame.LoadInterface(MyScreen)
            
            elif f"Nb fruits {NbFruits}"==interfaceGame.getCurrentSelectedBox().getName():
                NbFruits=(NbFruits+1)%12
                interfaceGame.getCurrentSelectedBox().setName(f"Nb fruits {NbFruits}")
                MyScreen.Rectangle(interfaceGame.getCurrentSelectedBox().getPoint()+Point(1,1),interfaceGame.getCurrentSelectedBox().getWidth()-2,interfaceGame.getCurrentSelectedBox().getHeigth()-2,MyScreen.color(0,0,0),True)
                interfaceGame.LoadInterface(MyScreen)
                
            elif "WallKill"==interfaceGame.getCurrentSelectedBox().getName():
                if WallKill:
                    CaseWallKill.color = (255,0,0)
                    WallKill = False
                else:
                    CaseWallKill.color = (0,255,0)
                    WallKill=True
                interfaceGame.LoadInterface(MyScreen)
            elif "Play"==interfaceGame.getCurrentSelectedBox().getName():
                SnakeStart(MyScreen,colorList[colorListSelector],NbFruits,WallKill)
                MyScreen.Fill(MyScreen.color(0,0,0))
                interfaceGame.LoadInterface(MyScreen)
            
        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    interfaceGame.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0

def SnakeStart(MyScreen,color=None,FruitsNumber=2,WallKill=False):
    color = MyScreen.color(color[0],color[1],color[2])
    joystick = Joystick(26,27)
    ButtonL = Button(15)
    
    snake = Snake(MyScreen,color,WallKill)
    MyScreen.Fill(MyScreen.color(200,255,200))
    MyScreen.Rectangle(Point(0,300),480,20,MyScreen.color(0,0,0),True)
    for i in range(FruitsNumber):
        snake.spawnBonus()
    loop=True
    
    
    beeper= Beeper(13)
    music = Music(256,beeper)
    music.Loop(True)
    thread = Thread(ThreadMusic,())
    thread.setArgs((music,thread))
    thread.start()
    
    while loop:
        x,y=joystick.getDirections()
            
        if y=="Down" and (snake.getOrientation() == "right" or snake.getOrientation() == "left"): #bas
            snake.setOrientation("down")
        elif y=="Up" and (snake.getOrientation() == "right" or snake.getOrientation() == "left"): #haut
            snake.setOrientation("up")
        elif x=="Left" and (snake.getOrientation() == "up" or snake.getOrientation() == "down"): #gauche
            snake.setOrientation("left")
        elif x=="Right" and (snake.getOrientation() == "up" or snake.getOrientation() == "down"): #droite
            snake.setOrientation("right")
            
        if ButtonL.read():
            snake.setAlive(False)
            
        if not snake.getAlive():
            loop=False
        snake.OrientationMove()
        snake.affichage()
        sleep(0.1)
    
    music.Stop()
    MyScreen.Fill(MyScreen.color(0,0,0))
    MyScreen.Text(Point(10,100),"GAME OVER",MyScreen.color(128,128,128),4)
    MyScreen.Text(Point(10,140),f"score={snake.length-3}",MyScreen.color(128,128,128),3)
    sleep(5)
    return 0


def ThreadMusic(music,thread):
    music.Volume(1000)
    music.Play(MiiMusic())
    thread.killThread()
    


class Snake:
    def __init__(self,MyScreen,color,WallKill=False,orientation="right",x=2,y=0,length=3,MaxPosX=16,MaxPosY=10):
        """lengt is for the current lenght of the snake
            color is for the color of the snake made with the command display.color(r,g,b)
            orientation is an str : 'up','down','right','left'
            pos is for the current pos of the head of the snake
            MaxPosX/Y is for where the wall in x/y is
            WallKill is a bool for if hitting the wall kill you"""
        self.MyScreen = MyScreen
        self.Game = [
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                ]
        self.length = length
        self.color = color
        self.orientation = orientation
        self.x = x
        self.y = y
        self.MaxPosX = MaxPosX
        self.MaxPosY = MaxPosY
        self.WallKill = WallKill
        self.Alive = True
        self.reduceTail = True
    def getReduceTail(self):
        return self.reduceTail
    def setReduceTail(self,reduceTail):
        self.reduceTail=reduceTail
    def getAlive(self):
        return self.Alive
    def setAlive(self,Alive:bool):
        self.Alive=Alive
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,x:int):
        self.x = x
    def setY(self,y:int):
        self.y = y
    def getLength(self):
        return self.length
    def setLength(self,length:int):
        self.length = length
    def getColor(self):
        return self.color
    def setColor(self,color):
        self.color = color
    def getOrientation(self):
        return self.orientation
    def setOrientation(self,orientation):
        self.orientation = orientation
        
    def move(self,x:int,y:int):
        contact = self.moveCollideCheck(x,y) #Après le déplacement le serpent va t'il rencontrer quelque chose ?
        if type(contact)==str or contact>0: #if contact is != 0 #Si il rencontre quelque chose
            if type(contact)==int: #Si cette chose est sa queue
                self.setAlive(False) #Mort
            elif type(contact)==str: #Si cette chose est un str
                if contact=="Bonus":  #Si Bonus
                    self.setLength(self.getLength()+1) #Aggrandissement longueur queue
                    self.Game[self.y][self.x]=self.getLength()
                    self.x= (x+self.x)%self.MaxPosX
                    self.y= (y+self.y)%self.MaxPosY
                    self.Game[self.y][self.x]="Snake"
                    self.spawnBonus()
                    
        else: #Si aucun obstacle
            if self.WallKill and self.moveCollideWallCheck(x,y): #Détection collision mur et mort potentielle
                self.setAlive(False) #Mort
                    
            else: #Si toute va bien
                self.AgingTail(-1)
                self.Game[self.y][self.x]=self.getLength()
                self.x= (x+self.x)%self.MaxPosX
                self.y= (y+self.y)%self.MaxPosY
                self.Game[self.y][self.x]="Snake"
            
    def moveCollideCheck(self,x:int,y:int): #return anything where we may collide
        return self.Game[(self.y+y)%self.MaxPosY][(self.x+x)%self.MaxPosX]
    
    def moveCollideWallCheck(self,x:int,y:int): #Check if any wall has been collided
        return ((self.y+y>=self.MaxPosY) or (self.x+x>=self.MaxPosX) or (self.y+y<0) or (self.x+x<0))
    
    def AgingTail(self,n:int): #Negative number = Aging, Positive number = Rejunevate
        for x in range(len(self.Game[0])):
            for y in range(len(self.Game)):
                if type(self.Game[y][x])==int and self.Game[y][x]>0:
                    self.Game[y][x] += n

    def OrientationMove(self):
        Orientation = self.getOrientation()
        if Orientation=="up" :
            self.move(0,-1)
        elif Orientation=="down" :
            self.move(0,1)
        elif Orientation=="right":
            self.move(1,0)
        elif Orientation=="left":
            self.move(-1,0)
    
    def spawnBonus(self):
        L=[]
        for Y in range(len(self.Game)):
            for X in range(len(self.Game[0])):
                if (self.Game[Y][X]==-1):
                    L.append((X,Y))
        if len(L)>0:
            n=randint(0,len(L))
            x,y = L[n-1][0],L[n-1][1]
            self.Game[y][x]="Bonus"

        
    def affichage(self):
        for i in range(len(self.Game)):
            for j in range(len(self.Game[0])):
                if type(self.Game[i][j])==int and self.Game[i][j]>=self.getLength():
                    self.MyScreen.Rectangle(Point(j*30+2,i*30+2),26,26,self.MyScreen.color(128,255,128),True)
                    
                elif type(self.Game[i][j])==int and self.Game[i][j]==0:
                    self.Game[i][j]=-1
                    self.MyScreen.Rectangle(Point(j*30,i*30),30,30,self.MyScreen.color(200,255,200),True)
                    
                elif type(self.Game[i][j])==str and self.Game[i][j]=="Snake":
                    self.MyScreen.Rectangle(Point(j*30,i*30),30,30,self.getColor(),True)
                    
                elif type(self.Game[i][j])==str and self.Game[i][j]=="Bonus":
                    self.MyScreen.Rectangle(Point(j*30+1,i*30+5),28,23,self.MyScreen.color(255,0,0),True)
                    self.MyScreen.Rectangle(Point(j*30+8,i*30),14,5,self.MyScreen.color(0,255,0),True)

