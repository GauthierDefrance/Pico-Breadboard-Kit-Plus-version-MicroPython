#screen by Gauthier Defrance 07/09/2024
from machine import Pin, SPI
import st7789_base, st7789_ext
from point import Point
#---------------------------------------
#Code based on the library st7789_base (From https://github.com/devbis/st7789py_mpy)
# and st7789_ext (From https://github.com/antirez/ST77xx-pure-MP)
#Thank to Ivan Belokobylskiy and Salvatore Sanfilippo
#---------------------------------------

#This library has been made by a newbie
#It will probably not be very efficient.
#Feel free to use it and modify it.
#I made it so using st7789 related library would be easier.

#---------------------------------------
#I refer to MyScreen in the comments.
#MyScreen is just a name that can be changed by anything you want.

#The way you should create your object, first create it and iniatilize it.
#MyScreen = Screen(2,3,4,5,6,7,480,320)
#MyScreen.init()

#When a color attribute is asked, use :  MyScreen.color(r,g,b)

#Point are just object with x and y attributes and getX(),getY() function.
#you can use any of your own made class with thoses attributes and function and it will probably work.

class Screen:
    def __init__(self,sck,mosi,miso,cs,dc,reset,W,H,landscape=True, mirror_x=False, mirror_y=False, is_bgr=False, xstart = None, ystart = None, inversion = False):
        
        self.landscape = landscape
        self.mirror_x = mirror_x
        self.mirror_y = mirror_y
        self.is_bgr=is_bgr
        self.xstart=xstart
        self.ystart=ystart
        self.inversion=inversion
        
        self.sck=Pin(sck, Pin.OUT)
        self.mosi=Pin(mosi, Pin.OUT)
        self.miso=Pin(miso, Pin.OUT)
        self.W = W
        self.H = H
        self.reset = Pin(reset, Pin.OUT)
        self.dc = Pin(dc, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.spi = SPI(0, baudrate=4000000, phase=0, polarity=0, bits=8, sck=self.sck, mosi=self.mosi, miso=self.miso)
        self.display = st7789_ext.ST7789(
        self.spi,
        self.W,
        self.H,
        self.reset,
        self.dc,
        self.cs
        )
        
        self.displayMono=None
        
    # Create a color by adjusting the RGB values    
    def color(self,r,g,b):
        """r for red, g for green and b for blue.
            This function return essential data."""
        return self.display.color(255-b, 255-g, 255-r)
    
    #-------------------------------------------
    # Standard display section
    # and usefull tools
    #-------------------------------------------
    
    # Initialize the display with current settings
    #You can't load anything using Mono without doing that first
    def init(self):
        self.display.init(self.landscape, self.mirror_x, self.mirror_y, self.is_bgr, self.xstart , self.ystart , self.inversion )
    
    def Sleep(self):
        self.display.sleep_mode(True)
    
    def WakeUp(self):
        self.display.sleep_mode(False)
    # Draw a pixel at PointA with the given color
    def Pixel(self,PointA,color):
        """Show a pixel of a certain color at a certain point of the screen."""
        self.display.pixel(PointA.getX(),PointA.getY(),color)
    
    
    # Fill the screen with a single color
    def Fill(self,color):
        self.display.fill(color)
        
        
    # Draw a line from PointA to PointB with the given color    
    def Line(self,PointA,PointB,color):
        self.display.line(PointA.getX(),PointA.getY(),PointB.getX(),PointB.getY(),color)
        
        
    # Draw a triangle using three points and a color, with optional fill
    def Triangle(self,PointA,PointB,PointC,color,fill=False):
        self.display.triangle( PointA.getX(),PointA.getY(), PointB.getX(), PointB.getY(), PointC.getX(), PointC.getY(), color, fill)
            
            
    # Draw a circle at PointA with the given radius and color, with optional fill        
    def Circle(self,PointA,radius,color,fill=False):
        self.display.circle(PointA.getX(), PointA.getY(), radius, color, fill)
    
    # Draw a rectangle from PointA with given width and height, with optional fill
    def Rectangle(self,PointA,W,H,color,fill=False):
        """PointA is an object with a x and y attributes.
            W and H are for the Width and Heigth of the Rectangle
            color is obtained by using MyScreen.color(r,g,b)
            """
        self.display.rect(PointA.getX(),PointA.getY(),W,H,color,fill)
    
    
    # Display text at PointA with the specified foreground color and optional background color
    def Text(self,PointA,text,fgcolor,upscaling=2,bgcolor=None):
        """PointA is an object with a x and y attributes.
            text is a chain of one or more character
            fgcolor is obtained by using MyScreen.color(r,g,b)
            it's for the color of the text
            upscaling allow to change the size of the text
            bgcolor allow to change the background color."""
        self.display.upscaled_text(PointA.getX(),PointA.getY(),text,fgcolor,bgcolor,upscaling)
     
     
    # Set a window for the display between PointA and PointB
    def Set_window(self, PointA,PointB):
        """Allow to change the size of the windows you want to works with.
            Can be very usefull if you only need a small part of the screen.
            PointA and PointB are object that possesses an x and y value."""
        self.display.set_window(PointA.getX(), PointA.getY(), PointB.getX(), PointB.getX())
    
    
    
    
    #To use this tool you will need to upload small .rgb565 image on your raspberry pico.
    #How do you get .rgb565 image ?
    #You can use the ImageConverterResizer code. You can't use it on your pico. It isn't powerfull enough.
    #This program use pill in order to converts and resize your image. So you need another library with it (i know lame...)
    #You will need Pillow for that.
    #Once you converted your png image, be sure that you know it's size, it's really important.
    #You need to know the height and witdh of the .rbg565 image in order to correctly make it appear on your screen.
    # A .rgb565 image has no metadata, so the size and width must be specified!
    
    #The call of this function should look like this :
    #YourObjectName.display_image('ImageName.rgb565',200(The height of the image),250(the widht of the image),P (The coordinates, optional))
    def display_image(self,filename:str,height:int,width:int,PointA=None):
        """filename is for an str that will be where is your file and how is it called on the raspberry pi pico.
            height and width is for the height and width of the .rgb565,
            be aware that if you resized it you will have to take that value here."""
        if PointA!=None:
            X=PointA.getX()
            Y=PointA.getY()
        else: X,Y=0,0
        with open(filename, 'rb') as f:
            for y in range(height):
                for x in range(width):
                    color_data = f.read(2)  # Read 2 bytes for each pixel (RGB565)
                    if len(color_data) == 2:
                        self.display.pixel(x+X, y+Y, color_data)
    
    #-----------------------------------------
    # Monochrome section with buffer    
    #-----------------------------------------
    
    # Initialize a display in monochrome mode
    #You can't load anything using Mono without doing that first
    def initMono(self):
        """Initalize an objet : displayMono that can only load black and white, but it's faster and has a framebuffer.
            You shouldn't use it for RGB because the RAM of the pico is not high enough."""
        self.displayMono = st7789_ext.ST7789(self.spi,self.W,self.H,self.reset,self.dc,self.cs)
        
        self.displayMono.init(self.landscape, self.mirror_x, self.mirror_y, self.is_bgr, self.xstart , self.ystart , self.inversion )
        
        self.displayMono.enable_framebuffer(mono=True)
    
    # A checkerboard pattern
    def echequier(self):
        """Generate a checkerboard pattern, purely for exemple."""
        if self.displayMono!=None:
            # Activate the framebuffer in monochrome mode
            self.displayMono.enable_framebuffer(mono=True)

            # Fill the framebuffer with a simple monochrome pattern (1-bit per pixel)
            for y in range(self.displayMono.height):
                for x in range(self.displayMono.width):
                    # Example of drawing a checkerboard pattern
                    if (x // 10) % 2 == (y // 10) % 2:
                        self.displayMono.fb.pixel(x, y, 1)  # Dessiner un pixel en blanc (1)
                    else:
                        self.displayMono.fb.pixel(x, y, 0)  # Dessiner un pixel en noir (0)

            # Transfer the framebuffer content to the screen using fast_mono_to_rgb
            self.displayMono.show_mono()
        else:
            print("Mono screen not initialised !")
    #
    #Fill free to make your own function for the Mono display !
    #
    