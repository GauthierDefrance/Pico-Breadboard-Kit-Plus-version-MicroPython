Hello,
if you want to try out the code on your own Raspberry Pi Pico,
you have to uppload all the files in this folder (except for the ReadMe.txt).
Then, normally once powered it should automatically launch the Main() function in 
main.py .

boot.py : is checking that the beeper, leds and RGB led are correctly turned off.
main.py : is the main program, it will use other lib such as MenuPlay.py in order
		  to make accessible Game, Music and settings.

rpimg.rgb565 : is used for the splash screen by default
pillar.rgb565 : is used by the game Tetris for decor
data.txt : is a file where is stocked the data of if the splash screen should turn on.
lib : is a folder where all the usefull code is.