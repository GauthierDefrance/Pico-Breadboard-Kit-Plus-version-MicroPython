#case by Gauthier Defrance 08/09/2024
from point import Point
from screen import *

#This library help create Case objects.
#They acts as box for the interface.
#They can :
# - Change color if selected
# - Have text displayed in them
# - Launch function if needed


class Case:
    def __init__(self,PointA,width,heigth,name="default",color=(0,0,0),color2=(20,20,20),function=None):
        """PointA is an object with two main function : getX() and getY().
            width and heigth are data for the size of the boxe when you want to load it on your screen.
            name is purely optional, help identifie the Case objects.
            color is the main color of the box, color2 is the secondary color.
            function is the function called when you use a certain methods."""
        self.PointA= PointA
        self.width = width
        self.heigth= heigth
        self.color = color
        self.color2 = color2
        self.name = name
        self.function = function
        self.Offx,self.Offy=0,0
        self.size = 2
    
    def getName(self):
        """Return the name of the class."""
        return self.name
    
    def getPoint(self):
        """Return a Point object."""
        return self.PointA
    
    def getWidth(self):
        """Return the width of the object."""
        return self.width
    
    def getHeigth(self):
        """Return the heigth of the object."""
        return self.heigth
    
    def setName(self,text):
        """Change the name of the object."""
        self.name = text
        
    def setSizeText(self,size):
        """Change the size of the text."""
        self.size = size
    
    def setOffXY(self,x,y):
        """Change where the text will appear in the box."""
        self.Offx,self.Offy=x,y
    
    def affichage(self,MyScreen,color=None):
        """MyScreen is an object of the screen library. It need to be initialized before doing anything !
            color is purely optionnal, in case you want to load another color for the box."""
        r,g,b = self.colorConverter(color)
        MyScreen.Rectangle(self.PointA,self.width,self.heigth,MyScreen.color(r,g,b))
    
    def affichageSecondary(self,MyScreen,color=None):
        """MyScreen is an object of the screen library. It need to be initialized before doing anything !
            color is purely optionnal, in case you want to load another color for the box.
            This function load per default the secondary color."""
        r,g,b = self.colorConverter2(color)
        self.affichage(MyScreen,(r,g,b))
        
    def affichageText(self,MyScreen,text,color=None):
        """This function load a text inside the box.
            Per default it's color is the same as the box.
            You can increase the size of the text.
            Offx and Offy are there in case you want the text to be more inside the boxe and by how much."""
        r,g,b = self.colorConverter(color)
        MyScreen.Text(self.PointA+Point(self.Offx,self.Offy),text,MyScreen.color(r,g,b),self.size)
        
    def LaunchFunction(self):
        """Launch the function that is associated to this Case object."""
        if self.function!=None:
            self.function()
        else:
            print("Can't launch this function.")
            
    def colorConverter(self,color=None):
        """Return a r,g,b color.
            by default return the main color of the box."""
        if color==None:
            r,g,b = self.color
        else:
            r,g,b = color
        return r,g,b
    
    def colorConverter2(self,color=None):
        """Return a r,g,b color.
            by default return the secondary color of the box."""
        if color==None:
            r,g,b = self.color2
        else:
            r,g,b = color
        return r,g,b