import pygame, led, sys, os, random, csv
import smbus
from pygame.locals import *

""" A very simple arcade shooter demo :)
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

adress = 0x48
LM75 = smbus.SMBus(1)

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialPort = sys.argv[1]
    print "INITIALIZING WITH USB-PORT: " + serialPort
    ledDisplay = led.teensy.TeensyDisplay(serialPort, fallbackSize)
else:
    print "INITIALIZING WITH SERVER DISPLAY AND SIMULATOR."
    ledDisplay = led.dsclient.DisplayServerClientDisplay('localhost', 8123, fallbackSize)

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 0 #1=alive; 0=dead


def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    pygame.joystick.init()
    
    # Initialize first joystick
    if pygame.joystick.get_count() > 0:
        stick = pygame.joystick.Joystick(0)
        stick.init()
    
    global gamestate

    scored = False
    # Clear event list before starting the game
    pygame.event.clear()

    while True:

        # Process event queue
        for pgevent in pygame.event.get():
            if pgevent.type == QUIT:
                pygame.quit()
                sys.exit()

            event = process_event(pgevent)

            # End the game
            if event.button == EXIT:
                gameover = True

            # Keypresses on keyboard and joystick axis motions / button presses
            elif event.type == PUSH:
                # Movements
                if event.button == UP:
                    pass
                elif event.button == DOWN:
                    pass
                elif event.button == RIGHT:
                    pass
                elif event.button == LEFT:
                    pass

                # Tower selection
            elif event.button == B2:
                pass

                # Tower placement
            elif event.button == P1:
                gameover = True

            # Only on Keyboard
            elif pgevent.type == KEYDOWN and pgevent.key == K_ESCAPE:
                gameover = True

            screen.fill(BLACK)
            font = pygame.font.SysFont("Arial", 16)
            text1 = font.render("Game over", 0, RED)
            text1pos = text1.get_rect()
            text1pos.midtop = (screen.get_rect().centerx, -1)
            screen.blit(text1,text1pos)
            text2 = font.render("Score: "+str(LM75.read_byte(adress)), 0, GREEN)
            text2pos = text2.get_rect()
            text2pos.midbottom = (screen.get_rect().centerx, 21)
            screen.blit(text2,text2pos)

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
