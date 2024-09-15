#interface by Gauthier Defrance 08/09/2024
from case import *

#---------------
#This code allow to create a very basic interface
#It will create a 2D list of basically button
#You can easily change which button is currently selected by using the MyInterface.nextX(n) and MyInterface.nextY(n) function.
#If you use MyInterface.Select() it will try to launch the function that is associated to the case.
#---------------

class Interface:
    #BoxList is a list of list :
    #[[Case1,Case2],
    #[Case3,Case4]]
    def __init__(self,BoxList:list,name=None):
        self.BoxList=BoxList
        self.name = name
        self.selectorX = 0
        self.selectorY = 0
    
    def reinit(self): #Renit the selector
        self.selectorX = 0
        self.selectorY = 0
    
    def getCurrentSelectedBox(self):
        """Return the currently selected box"""
        return self.BoxList[self.selectorY][self.selectorX]
    
    def getBoxList(self):
        """Return the list of all the box this interface have."""
        return self.BoxList
    
    def LoadInterface(self,MyScreen):
        """Load the text and the body of the boxs."""
        for y in range(len(self.BoxList)):
            for x in range(len(self.BoxList[y])):
                if self.selectorX==x and self.selectorY==y:
                    self.BoxList[y][x].affichageSecondary(MyScreen,self.BoxList[y][x].color2)
                    
                else:
                    self.BoxList[y][x].affichage(MyScreen)
                
                self.BoxList[y][x].affichageText(MyScreen, self.BoxList[y][x].getName(),(int(round(self.BoxList[y][x].color[0]*0.9)),int(round(self.BoxList[y][x].color[1]*0.9)),int(round(self.BoxList[y][x].color[2]*0.9)))) #Loading the name of the Case
                
    def nextX(self,n):
        """Allow to change the current selected box in x."""
        self.selectorX=(self.selectorX+n)%len(self.BoxList[self.selectorY])
        
    def nextY(self,n):
        """Allow to change the current selected box in y."""
        self.selectorY=(self.selectorY+n)%len(self.BoxList)
        self.selectorX=(self.selectorX)%len(self.BoxList[self.selectorY])
        
    def Select(self):
        """Activate the function of the selected box."""
        self.BoxList[self.selectorY][self.selectorX].LaunchFunction()
        
    def __str__(self):
        """Return an str schematic of the current menu."""
        text = f"Interface :"
        for y in range(len(self.BoxList)):
            text+="\n"
            for x in range(len(self.BoxList[y])):
                text+= f"  {self.BoxList[y][x].getName()}  "
        return text