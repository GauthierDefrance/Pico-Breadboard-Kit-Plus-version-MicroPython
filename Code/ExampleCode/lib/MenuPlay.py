#Play menu
from interface import * #Help create easily different kind of interface easily on the screen.

##---Programmes---
from point import Point #Allow to create the Point object pretty usefull.
from utime import sleep #Make the program wait a bit
from control import Control

##---Périphériques---
from button import * #For creating Button object
from joystick import * #For creating Joystick object


def MenuGame(MyScreen):
    ##---Joystick Presets---
    joystick = Joystick(26,27)

    ##---Button Presets---
    ButtonL = Button(15)
    ButtonR = Button(14)


    ##---Play Menu ---
    CaseSpaceInvaders = Case(Point(0,0),160,100,"Sp.Inv.",(254,254,254),(0,200,0),None)
    CasePiano = Case(Point(161,0),158,100,"Piano",(254,254,254),(0,200,0),None)
    CasePong = Case(Point(320,0),160,100,"Pong",(254,254,254),(0,200,0),None)
    CaseTetris = Case(Point(0,101),160,100,"Tetris",(254,254,254),(0,200,0),None)
    CaseConnectFour = Case(Point(161,101),158,100,"Co.4",(254,254,254),(0,200,0),None)
    CaseSnake = Case(Point(320,101),160,100,"Snake",(254,254,254),(0,200,0),None)

    CaseBack = Case(Point(160,250),160,100,"Back",(254,254,254),(0,200,0),None)

    CaseSpaceInvaders.setOffXY(20,40)
    CasePiano.setOffXY(20,40)
    CasePong.setOffXY(20,40)
    CaseTetris.setOffXY(20,40)
    CaseConnectFour.setOffXY(20,40)
    CaseSnake.setOffXY(20,40)

    CaseBack.setOffXY(50,40)

    ListPlayMenu = [[CaseSpaceInvaders,CasePiano,CasePong],
                    [CaseTetris,CaseConnectFour,CaseSnake],
                     [CaseBack]]

    interfaceGame = Interface(ListPlayMenu,"MenuGame")

    MyScreen.Fill(MyScreen.color(0,0,0))
    interfaceGame.LoadInterface(MyScreen)
    loop = True
    while loop:
        Control(MyScreen,joystick,interfaceGame) 
        if ButtonR.read():
            if "Back"==interfaceGame.getCurrentSelectedBox().getName():
                loop=False
                
            elif "Sp.Inv."==interfaceGame.getCurrentSelectedBox().getName():
                import spaceinvaders
                spaceinvaders.MenuSpaceInvaders(MyScreen)
                del spaceinvaders  # Libération de la mémoire après utilisation
                interfaceGame.reinit()
                interfaceGame.LoadInterface(MyScreen)
                
            elif "Piano"==interfaceGame.getCurrentSelectedBox().getName():
                import piano
                piano.MenuPiano(MyScreen)
                del piano  # Libération de la mémoire après utilisation
                interfaceGame.reinit()
                interfaceGame.LoadInterface(MyScreen)
            
            elif "Pong"==interfaceGame.getCurrentSelectedBox().getName():
                import pong
                pong.MenuPong(MyScreen)
                del pong  # Libération de la mémoire après utilisation
                interfaceGame.reinit()
                interfaceGame.LoadInterface(MyScreen)
                
            elif "Tetris"==interfaceGame.getCurrentSelectedBox().getName():
                import tetris
                tetris.MenuTetris(MyScreen)
                del tetris  # Libération de la mémoire après utilisation
                interfaceGame.reinit()
                interfaceGame.LoadInterface(MyScreen)
                
            elif "Co.4"==interfaceGame.getCurrentSelectedBox().getName():
                import connectfour
                connectfour.MenuCoF(MyScreen)
                del connectfour  # Libération de la mémoire après utilisation
                interfaceGame.reinit()
                interfaceGame.LoadInterface(MyScreen)       
                
            elif "Snake"==interfaceGame.getCurrentSelectedBox().getName():
                import snake
                snake.MenuSnake(MyScreen)
                del snake  # Libération de la mémoire après utilisation
                interfaceGame.reinit()
                interfaceGame.LoadInterface(MyScreen)
                
       
        elif ButtonL.read():
            loop=False
        sleep(0.3)
    
    interfaceGame.reinit()
    MyScreen.Fill(MyScreen.color(0,0,0))
    return 0
