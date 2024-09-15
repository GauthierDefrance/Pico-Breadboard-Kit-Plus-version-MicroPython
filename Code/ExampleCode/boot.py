from led import *
from beeper import *
from rgbled import *
#Will blink once to indicate that the board is booting normally.


def Start():
    """Killing artifact from last session."""
    #Turning off all the leds, RGB, and the beeper.
    led = Led('LED')
    led16 = Led(16)
    led17 =Led(17)
    rgb = RGBLed(12)
    beeper = Beeper(13)
    led.off()
    led16.off()
    led17.off()
    beeper.bequiet()
    rgb.quickColor(0,0,0)
    #
    
    #Testing the on board led, it should blink if everything is okay.
    led.blink(1)
    led.off()
    #
    
    #Start the main programs
    import main
    main.Main()
    del main
    #

Start()
