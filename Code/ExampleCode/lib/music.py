#music by Gauthier Defrance 08/09/2024
#Songs from https://github.com/robsoncouto/arduino-songs
from musicdata import * #This is where the songs are saved thoses musics are the property of other peoples !
from beeper import *
from utime import sleep
#The idea of the code come partially from here : https://github.com/robsoncouto/arduino-songs


# change this to make the song slower or faster
#tempo=256


#How to use it example:

#YourObject      the speed, the Beeper object at what pin.
#MyMusic = Music(tempo,Beeper(13))

#Here you can modify the Volume of the devices 1000 is nice, you can go up to 65536.
#If you modify this value to 0 the buzzer will stop making sounds.
#MyMusic.Volume(1000)

#Here you can select a music among a ton of music in the library musicdata
#You can add your own. The music is just a tuple and the actual size of a music is len(msusic)//2.
#MyMusic.Play(YourMusicName())

class Music:
    def __init__(self,tempo,beeper):
        """Tempo for the speed of the music, beeper for the object which play sounds"""
        #That objects has some nice function.
        self.beeper = beeper
        self.music = ()
        self.tempo=tempo
        self.selector = 0
        self.play = False
        self.pause = False
        self.loop = False
        self.volume = 0
        
    def Play(self,music:tuple):
        """Main function that start a music.
            music is a tuple that goes by pairs : ( Frequency0,Duration0,...,FrequencyN,DurationN).
            You can play it in your mainthread but the program won't be able to do anything else than that.
            You should call this function with a thread.
            If you do, you will be able to loop the music, pause it, and stop it with your main Thread."""
        self.music = music
        #self.pause = False
        self.play=True
        self.selector=0
        start=True
        wholenote = (60 * 4) / self.tempo
        while (start or self.loop) and self.play:
            
            #Activate ONCE and then more while self.play is True and self.loop is true.
            if start:
                #Activate once.
                start=False
                
            for k in range(len(self.music)//2):
                #For loop that will read the music tuple
                self.selector = k #Optional, but tell where are we in the current music
                print("Pause :",self.pause)
                if self.pause: #Block the Thread in a loop while self.pause is True.
                    self.beeper.bequiet() #Just in case
                    while self.pause: #Pause loop
                        sleep(0.1) #You can add a print here so that the program tell he is in a loop.
                        if not self.play:
                            self.beeper.bequiet() #Just in case
                            break
                if not self.play:
                    #If self.play is false that means self.Stop() has been activated.
                    #Break from the for loop and after the While loop.
                    #Should end the programs
                    self.beeper.bequiet() #Just in case
                    break
                
                frequence = self.music[k*2] #Select the current frequency to play
                divider = self.music[k*2+1] #Select the time that note should be played
                if divider > 0:
                    noteDuration = wholenote/divider
                elif divider < 0:
                    noteDuration = wholenote/abs(divider)
                    noteDuration = noteDuration*1.5
                if frequence>0:
                    try:
                        self.beeper.beep(frequence,noteDuration*0.9) #Play the note
                    except:
                        print(frequence,k)
                    sleep(noteDuration)
                elif frequence==0:
                    sleep(noteDuration)
            self.beeper.bequiet() #Just in case
        print("End Music") #Print that the music ended
        self.play=False #Just in case
        self.beeper.bequiet() #Just in case
        
    def getVolume(self):
        return self.volume
    
    def getTempo(self):
        """Return the current speed of the music."""
        return self.tempo
    
    def setTempo(self,tempo):
        """Change the speed of the music."""
        self.tempo=tempo
    
    def Stop(self):
        """Stop the current song."""
        self.play=False
        self.beeper.bequiet()
        
    def Pause(self):
        """Pause the current song."""
        self.pause=True
        
    def Continue(self):
        """Unpause the current song."""
        self.pause = False
        
    def Loop(self,loop):
        """Activate the loop mode for the song."""
        self.loop = loop
        
    def Volume(self,volume):
        """Change the volume of the buzzer."""
        self.volume = volume
        self.beeper.Volume(volume)
    
    def isPaused(self):
        """Return a boolean telling if the music is paused."""
        return self.pause
    
    def isPlaying(self):
        """Return a boolean telling if it is playing music."""
        return self.play