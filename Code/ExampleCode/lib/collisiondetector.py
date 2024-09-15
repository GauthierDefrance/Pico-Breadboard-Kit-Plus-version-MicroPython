#collisiondetector by Gauthier Defrance 09/09/2024
from point import Point
from math import sqrt

#This class has two objects for detection of collision
#Rectangle is for objects that has the form of a rectangle.
#Same for Circle.

#You use "in" to know if two objects of the same type collide.
#Example :
# MyRectangleA in MyRectangleB
#It will return True if they are colliding, else False.
#Same for the Circle.

class Rectangle:
    def __init__(self,PointA:Point,width:int,heigth:int):
        self.PointA = PointA
        self.width = width
        self.heigth = heigth
    
    def setPoint(self,PointA):
        self.PointA = PointA
    
    def getPoint(self) -> Point:
        """Return a Point object."""
        return self.PointA
    
    def getWH(self) -> tuple:
        """Return a tuple with the width and heigth."""
        return self.width,self.heigth
    
    def __contains__(self,other:Rectangle) -> bool:
        """Test the collision."""
        Colliding = False
        
        r1x_left = self.PointA.x
        r1x_right = self.PointA.x + self.width
        r1y_top = self.PointA.y
        r1y_bottom = self.PointA.y +self.heigth
        
        r2x_left = other.PointA.x
        r2x_right = other.PointA.x+other.width
        r2y_top = other.PointA.y
        r2y_bottom = other.PointA.y+other.heigth
        
        if r1x_right>r2x_left and r1x_left<r2x_right and r1y_bottom>r2y_top and r1y_top<r2y_bottom:
            Colliding = True
        return Colliding
    
class Circle:
    def __init__(self,PointA:Point,radius:int):
        self.PointA = PointA
        self.radius = radius
    
    def getRadius(self) -> int:
        """Return the radius of the circle."""
        return self.radius
        
    def getPoint(self) -> Point:
        """Return a Point object."""
        return self.PointA
    
    def __contains__(self,other:Body) -> bool:
        """Test the collision."""
        answer = False
        if sqrt((other.getPoint().getX()-self.getPoint().getX())**2 + (other.getPoint().getY()-self.getPoint().getY())**2)<=other.getRadius()+self.getRadius():
            anwser = True
        return answer
        
        
        