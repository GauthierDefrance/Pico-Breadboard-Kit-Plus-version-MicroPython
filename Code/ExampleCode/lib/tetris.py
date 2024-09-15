#Tetris
from interface import * #Help create easily different kind of interface easily on the screen.
from screen import *
##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control
from random import randint
from beeper import *
from music import *
from thready import * #Thready will allow us to play music while playing the game.


##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object


def MenuTetrisMessage():
    Vscreen = Screen(2,3,4,5,6,7,320,480,False,True)
    Vscreen.init()
    Vscreen.Fill(Vscreen.color(0,0,0))
    #Screen has been initialized
    Vscreen.Text(Point(30,100),"Please turn your screen",Vscreen.color(128,128,128),1)
    Vscreen.Text(Point(30,120),"In order to play this game.",Vscreen.color(128,128,128),1)
    Vscreen.Text(Point(30,140),"Have fun !",Vscreen.color(128,128,128),3)
    sleep(5)
    Vscreen.Fill(Vscreen.color(0,0,0))
    return Vscreen

def MenuTetris(MyScreen):
    
    
    MyScreen.Fill(MyScreen.color(0,0,0))
    Vscreen = MenuTetrisMessage()
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    
    
    ##---Play Menu ---
    CasePlay = Case(Point(60,100),200,100,"Play",(254,254,254),(0,200,0),None)
    CaseBack = Case(Point(60,250),200,100,"Quit",(254,254,254),(0,200,0),None)
    CasePlay.setOffXY(50,40)
    CaseBack.setOffXY(50,40)

    ListPlayTetris = [[CasePlay,CaseBack]]

    interfaceGame = Interface(ListPlayTetris,"MenuGame")

    Vscreen.Fill(Vscreen.color(0,0,0))
    interfaceGame.LoadInterface(Vscreen)
    loop = True
    while loop:
        Control(Vscreen,joystick,interfaceGame) 
        if ButtonR.read():
            if "Quit"==interfaceGame.getCurrentSelectedBox().getName():
                loop=False
                
            elif "Play"==interfaceGame.getCurrentSelectedBox().getName():
                Tetris(Vscreen,joystick,ButtonR,ButtonL)
                Vscreen.Fill(Vscreen.color(0,0,0))
                interfaceGame.LoadInterface(Vscreen)
            
        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    interfaceGame.reinit()
    Vscreen.Fill(Vscreen.color(0,0,0))
    MyScreen = Screen(2,3,4,5,6,7,480,320)
    MyScreen.init()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0

def ThreadMusic(music,thread):
    music.Volume(1000)
    music.Play(TetrisMusic())
    thread.killThread()

def Tetris(MyScreen,joystick,ButtonR,ButtonL):
    MyScreen.Fill(MyScreen.color(0,0,0))
    img = "pillar.rgb565"
    imgWH = (60,460)
    imgP1 = Point(0,0)
    imgP2 = Point(320-imgWH[0],0)
    MyScreen.display_image(img,imgWH[1],imgWH[0],imgP1)
    MyScreen.display_image(img,imgWH[1],imgWH[0],imgP2)
    tetris = FallingObject(MyScreen,)
    tetris.spawnBlock()
    tetris.gameActualize(True)
    tetris.affichage()
    sleep(0.5)
    buttonL = Pin(15,Pin.IN) #Bouton droit : Annuler
    buttonR = Pin(14,Pin.IN) #Bouton droit : Valider
    #Joystick
    YAxis = ADC(Pin(27))
    XAxis = ADC(Pin(26))
    
    
    beeper= Beeper(13)
    music = Music(256,beeper)
    music.Loop(True)
    thread = Thread(ThreadMusic,())
    thread.setArgs((music,thread))
    thread.start()
    
    
    while tetris.Alive:
        x,y=joystick.getDirections()
        tetris.fall()
        if not buttonL():
            tetris.Alive=False
            
        if not buttonR():
            tetris.rotate()
            
        if x=="Right":
            tetris.fall()
        #elif x=="Left":
        #   pass
        if y=="Up":
            tetris.MoveH(1)
        elif y=="Down":
            tetris.MoveH(-1)
            
        tetris.fall()    
        tetris.affichage()
        sleep(0.6)
    music.Stop()
    MyScreen.Fill(MyScreen.color(0,0,0))
    MyScreen.Text(Point(10,100),"GAME OVER",MyScreen.color(128,128,128),4)
    MyScreen.Text(Point(10,140),f"score={tetris.score}",MyScreen.color(128,128,128),3)
    sleep(5)
    return 0


class FallingObject:
    def __init__(self,MyScreen):
        self.colorList = [MyScreen.color(255,182,193),
                          MyScreen.color(255,255,0),
                          MyScreen.color(173,216,230),
                          MyScreen.color(0,0,255),
                          MyScreen.color(255,165,0),
                          MyScreen.color(0,255,0),
                          MyScreen.color(255,0,0)]
        
        #pink
        T = [[[0,1,0],[1,1,1],[0,0,0]],[[0,1,0],[0,1,1],[0,1,0]],[[0,0,0],[1,1,1],[0,1,0]],[[0,1,0],[1,1,0],[0,1,0]],]
        #Yellow
        O = [[[0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]], [[0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]]]
        #Light Blue
        I = [[[0, 3, 0, 0], [0, 3, 0, 0], [0, 3, 0, 0], [0, 3, 0, 0]], [[0, 0, 0, 0], [3, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [3, 3, 3, 3], [0, 0, 0, 0]]]
        #Blue
        J = [[[0, 0, 0], [4, 0, 0], [4, 4, 4]], [[0, 0, 4], [0, 0, 4], [0, 4, 4]], [[4, 4, 4], [0, 0, 4], [0, 0, 0]], [[4, 4, 0], [4, 0, 0], [4, 0, 0]]]
        #Orange
        L = [[[5, 5, 5], [5, 0, 0], [0, 0, 0]], [[5, 0, 0], [5, 0, 0], [5, 5, 0]], [[0, 0, 0], [0, 0, 5], [5, 5, 5]], [[0, 5, 5], [0, 0, 5], [0, 0, 5]]]
        #Green
        S = [[[0, 6, 6], [6, 6, 0], [0, 0, 0]], [[0, 6, 0], [0, 6, 6], [0, 0, 6]], [[0, 0, 0], [0, 6, 6], [6, 6, 0]], [[6, 0, 0], [6, 6, 0], [0, 6, 0]]]
        #Red
        Z = [[[7, 7, 0], [0, 7, 7], [0, 0, 0]], [[0, 0, 7], [0, 7, 7], [0, 7, 0]], [[0, 0, 0], [7, 7, 0], [0, 7, 7]], [[0, 7, 0], [7, 7, 0], [7, 0, 0]]]
        self.x=3    
        self.y=0
        self.MaxPosX=10
        self.MaxPosY=20
        self.BlockList= [T,O,I,J,L,S,Z]
        self.Alive = True
        self.score = 0
        self.MyScreen =MyScreen
        self.Game = [[0 for k in range(10)] for i in range(20)]
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getMaxPosX(self):
        return self.MaxPosX
    
    def getMaxPosY(self):
        return self.MaxPosY
    
    def setX(self,x):
        self.x=x
        
    def setY(self,y):
        self.y=y
        
    def getBlock(self):
        return self.Block
    
    def getBlockSelector(self):
        return self.BlockSelector
    
    def spawnBlock(self):
        self.linedelete()
        self.BlockSelector=0
        self.pickRandomForm()
        self.x=3
        self.y=0
        if not self.spawncheck():
            print("Mort")
            self.Alive = False

    def spawncheck(self):
        for Y in range(len(self.getBlock()[self.getBlockSelector()])):
            for X in range(len(self.getBlock()[self.getBlockSelector()][0])):
                if self.Game[Y+self.getY()][X+self.getX()]>0:
                    return False
        return True
        
    def pickRandomForm(self):    
        x = randint(0,len(self.BlockList)-1)
        self.Block = self.BlockList[x]
        
    def rotate(self):
        if self.rotatecheck():
            self.gameActualize(False)
            self.BlockSelector=(self.BlockSelector+1)%len(self.Block)
            self.gameActualize(True)
        
    def rotatecheck(self):
        BlockSelector = (self.BlockSelector+1)%len(self.Block)
        for Y in range(len(self.getBlock()[BlockSelector])):
            for X in range(len(self.getBlock()[BlockSelector][0])):
                if self.getBlock()[(BlockSelector)][Y][X]>0: #Si il y a un check à faire
                    if (len(self.getBlock()[BlockSelector])+self.getY()>19):
                        return False
                    elif (X+self.getX()<-1 or X+self.getX()>12-len(self.getBlock()[BlockSelector])):
                        return False
                    elif (self.Game[Y+self.getY()][X+self.getX()]>0)and not(self.getBlock()[(BlockSelector)][Y][X]==self.Game[Y+self.getY()][X+self.getX()] and self.getBlock()[(self.BlockSelector)][Y][X]==self.Game[Y+self.getY()][X+self.getX()]):
                        return False
                    
        return True
    
    def MoveV(self,n):
        self.setY(self.getY()+n)
        
    def MoveH(self,n):
        if self.wallcheck(n) and self.blockcheckH(n):
            self.gameActualize(False)
            self.setX(self.getX()+n)
            self.gameActualize(True)
            
    def fall(self):
        if self.blockcheckV():
            self.gameActualize(False)
            self.MoveV(1)
            self.gameActualize(True)
        else:
            self.spawnBlock()
            
    def gameActualize(self,create:bool):
        x=self.getX()
        y=self.getY()
        for Y in range(len(self.getBlock()[self.getBlockSelector()])):
            for X in range(len(self.getBlock()[self.getBlockSelector()][0])):
                if Y+y<20:
                    if self.getBlock()[self.getBlockSelector()][Y][X]>0 and not create:
                        self.Game[Y+y][X+x]=-1
                    elif self.getBlock()[self.getBlockSelector()][Y][X]>0 and create and (self.Game[Y+y][X+x]==-1 or self.Game[Y+y][X+x]==0):
                        self.Game[Y+y][X+x]=self.getBlock()[self.getBlockSelector()][Y][X]
        
    def wallcheck(self,n):
        for Y in range(len(self.getBlock()[self.getBlockSelector()])):
            for X in range(len(self.getBlock()[self.getBlockSelector()][0])):
                if self.getBlock()[self.getBlockSelector()][Y][X]>0:
                    if not((X+self.getX())>0 and (X+self.getX())<20):
                        return False
        
        return True
    
    def blockcheckV(self):
        for Y in range(len(self.getBlock()[self.getBlockSelector()])):
            for X in range(len(self.getBlock()[self.getBlockSelector()][0])):
                    if self.getBlock()[self.getBlockSelector()][Y][X]>0: #Est-ce que l'élément a besoin d'être testé.
                        if self.getY()+Y+1<len(self.Game) and (Y+self.getY()+1<len(self.Game)) and self.Game[Y+self.getY()+1][X+self.getX()]>0 : #Est-ce que l'élément en dessous existe
                            if Y+1>=len(self.getBlock()[self.getBlockSelector()]):
                                return False
                            elif (self.getBlock()[self.getBlockSelector()][Y+1][X]==0): #est-ce que l'élément en dessous fait partie de la structure
                                return False
                        if not(self.getY()+Y+1<len(self.Game)):
                            return False
        return True
        
    def blockcheckH(self,n):
        for Y in range(len(self.getBlock()[self.getBlockSelector()])):
            for X in range(len(self.getBlock()[self.getBlockSelector()][0])):
                    if self.getBlock()[self.getBlockSelector()][Y][X]>0: #Est-ce que l'élément a besoin d'être testé.
                        if (X+self.getX()+n<len(self.Game[0])) and self.Game[Y+self.getY()][X+self.getX()+n]>0 : #Est-ce que l'élément en n existe
                            if X+n>=len(self.getBlock()[self.getBlockSelector()][0]):
                                return False
                            elif (self.getBlock()[self.getBlockSelector()][Y][X+n]==0): #est-ce que l'élément en dessous fait partie de la structure
                                return False
                        if not(self.getX()+X+n<len(self.Game[0])):
                            return False
        return True
    
    def linedetect(self):
        for Y in range(len(self.Game)):
            if not(0 in self.Game[Y]):
                return (True,Y)
        return (False,None)
    
    def linedelete(self):
        x = self.linedetect()
        while x[0]:
            print("Ligne détecté")
            self.Game.pop(x[1])
            self.Game.insert(0,[0,0,0,0,0,0,0,0,0,0])
            self.setY(self.getY()+1)
            self.score+=1
            self.affichageComplet()
            x = self.linedetect()
        
        
    def affichage(self):
        for y in range(len(self.Game)):
            for x in range(len(self.Game[0])):
                if self.Game[y][x]>0:
                    self.MyScreen.Rectangle(Point(60+x*20,80+y*20),20,20,self.colorList[self.Game[y][x]-1],True)
                    #self.MyScreen.Rectangle(60+x*20,80+y*20,20,20,grey,False)
                elif self.Game[y][x]==-1:
                    self.Game[y][x]=0
                    self.MyScreen.Rectangle(Point(60+x*20,80+y*20),20,20,self.MyScreen.color(0,0,0),True)
                    
    def affichageComplet(self):
        for y in range(len(self.Game)):
            for x in range(len(self.Game[0])):
                if self.Game[y][x]>0:
                    self.MyScreen.Rectangle(Point(60+x*20,80+y*20),20,20,self.colorList[self.Game[y][x]-1],True)
                    #self.MyScreen.Rectangle(60+x*20,80+y*20,20,20,grey,False)
                elif self.Game[y][x]==0:
                    self.MyScreen.Rectangle(Point(60+x*20,80+y*20),20,20,self.MyScreen.color(0,0,0),True)   
        
        
        
    

