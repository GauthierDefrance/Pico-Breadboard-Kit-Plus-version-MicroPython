#homemade i don't think the way i kill thread is really good.
#Please don't use this in other codes.
#----------------------------------------------------------------------
#thready by Gauthier Defrance 06/09/2024
import _thread
from led import *
#An optional class to use the default _thread library on the raspberry pi pico W
#You can just use _thread instead

#----------------------------------------------------------------------


#Warning this can cause many many crash.
#Please be carefull with this
#AND DON'T FORGET TO KILL THE THREAD YOU CREATE
#Or atleast be able to kill them if you reboot your pico

class Thread:
    def __init__(self,function,args:tuple):
        """function is for the name of a function that will be launch by the Thread,
            args are for the arguments that will be taken for that function.
            args is a tuple."""
        self.function = function
        self.args = args
        self.mainId = _thread.get_ident()
        self.running = False
        self.led = Led('LED')
    def getArgs(self):
        """Return the current tuples set for the args of the function."""
        return self.args
    
    def setArgs(self,args:tuple):
        """Allow to change the args for the functions"""
        self.args=args
        
    def getFunction(self):
        """Return the current function where the Thread will start."""
        return self.function
    
    def setFunction(self,function):
        """"Allow to change the function where the Thread will start."""
        self.function = function
        
    def start(self):
        """Begin the Thread at the function with the args"""
        print(f"Thread start at the function : {self.function} with theses args : {self.args}.")
        if not self.running:
            self.led.on()
            _thread.start_new_thread(self.function,self.args)
        else:
            print("Already running.")
        
        
    def killThread(self):
        """Put this inside the function where the Thread will run at the moment you want the Thread to die."""
        
        #YOU MUST KILL THE THREAD AFTER EACH RUN.
        #Else the rp pico will need a hard reboot (disconnect it from power and connect it again).
        
        if self.mainId != _thread.get_ident():
            self.led.off()
            self.running=False
            #Small test just to be SURE you didn't kill the main thread, that would crash everything.
            try:
                print(f"⚠ Killing thread : {_thread.get_ident()} ⚠")
                _thread.exit()
            except:
                #print(case)
                #print here is purely optionnal, you can activate it in order to get an error message that will be skipped each time
                pass
            finally:
                print(f"Thread : {_thread.get_ident()} has been succesfully killed.")
        else:
            print(f"⚠️ You tried to kill the main thread ⚠️ \n Thread detected id is : {_thread.get_ident()}")

        
        
        