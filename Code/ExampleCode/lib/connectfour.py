#Connect Four made by Gauthier Defrance 14/09/2024
from interface import * #Help create easily different kind of interface easily on the screen.
from screen import *
##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object

def MenuCoF(MyScreen:Screen) -> False:
    """Function that start the Game Connect Four."""
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

    ListPlayCoF = [[CasePlay],
                    [CaseBack]]

    interfaceGame = Interface(ListPlayCoF,"MenuGame")

    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceGame.LoadInterface(MyScreen)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceGame) 
        if ButtonR.read():
            if "Quit"==interfaceGame.getCurrentSelectedBox().getName():
                loop=False
                
            elif "Play"==interfaceGame.getCurrentSelectedBox().getName():
                ConnectFour(MyScreen)
                MyScreen.Fill(MyScreen.color(0,0,0))
                interfaceGame.LoadInterface(MyScreen)
            
        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    interfaceGame.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0

def ConnectFour(MyScreen:Screen) -> False:
    MyScreen.Fill(MyScreen.color(0,0,0))
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)
    
    jeu = CoF(Point(65,20),50,MyScreen.color(255,0,0),MyScreen.color(0,0,255),"Red","Blue",MyScreen,MyScreen.color(255,255,255))
    jeu.LoadWall()
    
    currentP = jeu.player1
    jeu.LoadTriangle(currentP)
    win = "None"
    loop = True
    
    while loop==True:
        directionx,directiony=joystick.getDirections()
                   
        
        if directionx=="Right":
            jeu.UnloadTriangle()
            jeu.nextcolumn(1)
            jeu.LoadTriangle(currentP)
            
        elif directionx=="Left":
            jeu.UnloadTriangle()
            jeu.nextcolumn(-1)
            jeu.LoadTriangle(currentP)
            
        if ButtonR.read() and jeu.isPlaceableColumn(jeu.getColumnSelector()):
            jeu.place(currentP) 
            if currentP == jeu.player1: currentP = jeu.player2
            else:currentP = jeu.player1
            jeu.LoadTriangle(currentP)
            
            if jeu.CheckWin(jeu.player1):
                win = jeu.player1
                loop = False
                
            elif jeu.CheckWin(jeu.player2):
                win = jeu.player2
                loop=False
            
            if not jeu.isPlaceable():
                loop=False
            
        elif ButtonL.read():
            loop=False
        sleep(0.3)
        
    MyScreen.Fill(MyScreen.color(0,0,0))
    MyScreen.Text(Point(10,0),"GAME OVER",MyScreen.color(128,128,128),4)
    MyScreen.Text(Point(10,50),f"Victory of {win}",MyScreen.color(196,196,196),3)
    sleep(3)
    return 0

class CoF:
    def __init__(self,point,WH,p1Color,p2Color,player1,player2,MyScreen,color):
        self.Game = [[0 for i in range(7)] for k in range(6)]
        self.columnSelector = 0
        self.p1Color,self.p2Color = p1Color,p2Color
        self.player1=player1
        self.player2 = player2
        self.MyScreen = MyScreen
        self.point = point #Point of top left of the game
        self.width = WH #width of each box
        self.heigth = WH #heigth of each box
        self.color = color
        
    def LoadWall(self):
        """Load all the line of the wall of the game."""
        for Y in range(len(self.Game)+1):
            self.MyScreen.Line(self.point+Point(0,self.heigth*Y),
                               self.point+Point(self.width*len(self.Game[0]),self.heigth*Y),
                               self.color)
            
        for X in range(len(self.Game[0])+1):
            self.MyScreen.Line(self.point+Point(self.width*X,0),
                               self.point+Point(self.width*X,len(self.Game)*self.heigth),
                               self.color) 
                
    
    def UnloadTriangle(self):
        """Delete the triangle."""
        self.MyScreen.Triangle(self.point+Point(self.width*self.columnSelector,-20),
                               self.point+Point(self.width*(self.columnSelector+1),-20),
                               self.point+Point(int(round(self.width*(self.columnSelector+0.5))),-1),
                               self.MyScreen.color(0,0,0),True)
        
    def LoadTriangle(self,player):
        
        """Load a triangle with the color of the current player telling where the cursor is currently heading."""
        if player==self.player1:
            color = self.p1Color
        elif player==self.player2:    
            color = self.p2Color
        else:
            color = self.MyScreen.color(255,255,255)
        self.MyScreen.Triangle(self.point+Point(self.width*self.columnSelector,-20),
                               self.point+Point(self.width*(self.columnSelector+1),-20),
                               self.point+Point(int(round(self.width*(self.columnSelector+0.5))),-1),
                               color,True)
        
    def LoadToken(self) -> None:
        """Load all the token on the current Screen."""
        for Y in range(len(self.Game)):
            for X in range(len(self.Game[0])):
                if self.Game[Y][X]==self.player1:
                    self.MyScreen.Circle(self.point+Point(self.width*X+(self.width-2)//2,self.heigth*Y+(self.width-2)//2),(self.width-3)//2,self.p1Color,True)
                elif self.Game[Y][X]==self.player2:
                    self.MyScreen.Circle(self.point+Point(self.width*X+(self.width-2)//2,self.heigth*Y+(self.width-2)//2),(self.width-3)//2,self.p2Color,True)
    
    def LoadTokenPrecize(self,X,Y):
        """Load the token at the coords X,Y of the Game."""
        print(X,Y)
        if self.Game[Y][X]==self.player1:
            self.MyScreen.Circle(self.point+Point(self.width*X+(self.width-2)//2,self.heigth*(Y)+(self.width-2)//2),(self.width-3)//2,self.p1Color,True)
        elif self.Game[Y][X]==self.player2:
            self.MyScreen.Circle(self.point+Point(self.width*X+(self.width-2)//2,self.heigth*(Y)+(self.width-2)//2),(self.width-3)//2,self.p2Color,True)
                    
    def getColumnSelector(self) -> int:
        """Return the currently selected column."""
        return self.columnSelector
    
    def nextcolumn(self,n:int) -> None:
        """Allow to pick a different collum for where to place the token."""
        self.columnSelector = (self.columnSelector+n)%len(self.Game[0])
    
    def isPlaceable(self) -> bool:
        """Return True if you can stil play in any Column."""
        return 0 in self.Game[0]
    
    def isPlaceableColumn(self,n:int) -> bool:
        """Return True if there is still space in the current column."""
        return self.Game[0][n]==0
    
    def place(self,player) -> None:
        """Function that place a token."""
        for Y in range(len(self.Game)):
            if self.Game[Y][self.columnSelector]==0 and (Y==len(self.Game)-1 or self.Game[Y+1][self.columnSelector]!=0):
                self.Game[Y][self.columnSelector]=player
                self.LoadTokenPrecize(self.columnSelector,Y)
                break
            elif Y==(len(self.Game)-1):
                self.Game[Y][self.columnSelector]=player
                self.LoadTokenPrecize(self.columnSelector,Y)
                break
                
    def CheckWin(self,player) -> bool:
        """Return True if the player has won."""
        return self.checkH(player) or self.checkV(player) or self.checkDR(player) or self.checkDL(player)
    
    
    def checkH(self,player) -> bool:
        """Check if 4 token of the same player are aligned on the same line."""
        for Y in range(len(self.Game)):
            for X in range(len(self.Game[0])-3):
                if self.Game[Y][X]==player and self.Game[Y][X+1]==player and self.Game[Y][X+2]==player and self.Game[Y][X+3]==player:
                    return True
        return False
        
    def checkV(self,player) -> bool:
        """Check if 4 token of the same player are aligned on the same column."""
        for Y in range(len(self.Game)-3):
            for X in range(len(self.Game[0])):
                if self.Game[Y][X]==player and self.Game[Y+1][X]==player and self.Game[Y+2][X]==player and self.Game[Y+3][X]==player:
                    return True
        return False
        
    def checkDR(self,player) -> bool:
        """Check if 4 token of the same player are aligned on the same right diagonal."""
        for Y in range(len(self.Game)-3):
            for X in range(len(self.Game[0])-3):
                if self.Game[Y][X]==player and self.Game[Y+1][X+1]==player and self.Game[Y+2][X+2]==player and self.Game[Y+3][X+3]==player:
                    return True
        return False
    
    def checkDL(self,player) -> bool:
        """Check if 4 token of the same player are aligned on the same left diagonal."""
        for Y in range(len(self.Game)-3):
            for X in range(len(self.Game[0])-3):
                if self.Game[Y+3][X]==player and self.Game[Y+2][X+1]==player and self.Game[Y+1][X+2]==player and self.Game[Y][X+3]==player:
                    return True
        return False
