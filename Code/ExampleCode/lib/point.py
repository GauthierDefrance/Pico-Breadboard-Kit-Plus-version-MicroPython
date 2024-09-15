#Basic geometry
#point by Gauthier Defrance 07/09/2024

#An optional class to regroup x and y together
#You can add points and turn it into str for informations.

class Point:
    def __init__(self,x:int,y:int):
        self.x,self.y=x,y
        
    def setX(self,x:int):
        """Allow to change the current pos in X of the point."""
        self.x=x
    
    def setY(self,y:int):
        """Allow to change the current pos in Y of the point."""
        self.y=y
    
    def getX(self) -> int:
        """Return the X of the Point."""
        return self.x
    
    def getY(self) -> int:
        """Return the Y of the Point."""
        return self.y
    
    
    def __add__(self,other:Point) -> Point:
        """Allow to add two Point together."""
        return Point(self.x + other.x, self.y + other.y)
    
    def __str__(self) -> str:
        """If you write print(myPoint) it will return a nice text explaining what are the coordinates of the point."""
        return f"Object of type Point :\nx={self.x}\ny={self.y}"
        