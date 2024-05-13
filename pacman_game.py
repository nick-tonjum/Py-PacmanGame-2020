#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import sys
import pygame
import pygame.locals
from random import randint
from pygame import *

pygame.init()

eat_pellet_sound = pygame.mixer.Sound('eatpellet.ogg')
eat_powerup_sound = pygame.mixer.Sound('eatpowerup.ogg')
death_sound = pygame.mixer.Sound('death.ogg')
pygame.mixer.music.load('pactheme.ogg')

# Playing music on a loop (-1)
pygame.mixer.music.play(-1)


displaymode = 1
screensize = [760, 760]

#Game Options
start_time = 3 # Seconds from startup until the game starts.

tickrate = 45 # How many frames the game proceeds per second.
pacman_speed = 5 # How many pixels pacman will move every frame
shift_multiplier = 1.5 # When holding the turbo button (shift), pacman's speed is multiplied by this number
ghost_speed = 2 # How many pixels ghosts will move every frame
speed_increments = [1, 1] # After each level speeds will increase by this amount [pacman speed, ghost speed].
powerup_time = 300 # How many frames the powerup pellet will last
powerup_decrement = 10 # How many frames will be removed from the powerup time value after each level
resets = [20, 25, 50] # After how many levels should each value be reset [pacman speed, ghost speed, powerup time].
debug_info = 0
debug_font_size = 24
dumb_ghosts = 3 # How many "dumb" ghosts will spawn. These will move in random directions.
smart_ghosts = 1 # How many "smart" ghosts will spawn. These will target pacman.
pacman_spawn = [380, 540] # The coordinates where pacman will spawn at.
ghost_spawn = [380, 460] # The coordinates where the ghosts will spawn.
hitbox = 35 #Pac-Man's hitbox size (pixels)
pacman_lives = 3
joystick_threshold = 0.5


screeninfo = pygame.display.Info()
determinedssx = screeninfo.current_w
determinedssy = screeninfo.current_h
level = 1
score = 0
fpsClock = pygame.time.Clock()
background_color = (0,0,0)
start_time += 1
if displaymode == 1:
    screen = pygame.display.set_mode((screensize[0], screensize[1]))
elif displaymode == 2:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screensize = [determinedssx, determinedssy]



pygame.display.set_caption('Pac Man')
screen.fill(background_color)
pygame.display.flip()
running = True

pacchar = [pygame.image.load('pacman0.png'), pygame.image.load('pacman1.png'), pygame.image.load('pacman2.png')]
pacpos = pacman_spawn
pacdirection = 0
pacanim = 0
ghostanim = 0
pacmanmoving = False
ghostweaktime = 225
alive = True
ghostweak = 0
rgb = [255,15,15]
rgbcyclepos = 0

font = pygame.font.SysFont('FreeSerif', debug_font_size)

main_font = pygame.font.SysFont('FreeSerif', debug_font_size)
joysticks = []

def initializeJoysticks():
    global joysticks
    """Initialise all joysticks, returning a list of pygame.joystick.Joystick"""
    joysticks = []              # for returning

    # Initialise the Joystick sub-module
    pygame.joystick.init()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range( joystick_count ):
        joystick = pygame.joystick.Joystick( i )
        joystick.init()
        # NOTE: Some examples discard joysticks where the button-count
        #       is zero.  Maybe this is a common problem. 
        joysticks.append( joystick )

    # TODO: Print all the statistics about the joysticks
    if ( len( joysticks ) == 0 ):
        print( "No joysticks found" )
    else:
        for i,joystk in enumerate( joysticks ):
            print("Joystick %d is named [%s]" % ( i, joystk.get_name() ) )
            # etc.

    return joysticks


def draw_map(color):
    x = 80
    # Border
    pygame.draw.line(screen, color, (x,x),(600+x,x), 2)
    pygame.draw.line(screen, color, (x,x),(x,240+x), 2)
    pygame.draw.line(screen, color, (x,240+x),(0,240+x), 2)
    pygame.draw.line(screen, color, (0,360+x),(x,360+x), 2)
    pygame.draw.line(screen, color, (x,360+x),(x,600+x), 2)
    pygame.draw.line(screen, color, (x,600+x),(600+x,600+x), 2)
    pygame.draw.line(screen, color, (600+x,600+x),(600+x,360+x), 2)
    pygame.draw.line(screen, color, (600+x,360+x),(760,360+x), 2)
    pygame.draw.line(screen, color, (760,240+x),(600+x,240+x), 2)
    pygame.draw.line(screen, color, (600+x,240+x),(600+x,x), 2)
    # Top
    pygame.draw.line(screen, color, (40+x,40+x),(560+x,40+x), 2)
    # Top Left
    pygame.draw.line(screen, color, (40+x,40+x),(40+x,240+x), 2) 
    pygame.draw.line(screen, color, (40+x,240+x),(80+x,240+x), 2) 
    pygame.draw.line(screen, color, (80+x,240+x),(80+x,280+x), 2) 
    pygame.draw.line(screen, color, (80+x,280+x),(0,280+x), 2) 
    # Bottom Left
    pygame.draw.line(screen, color, (0,320+x),(80+x,320+x), 2)
    pygame.draw.line(screen, color, (80+x,320+x),(80+x,360+x), 2)
    pygame.draw.line(screen, color, (80+x,360+x),(40+x,360+x), 2)
    pygame.draw.line(screen, color, (40+x,360+x),(40+x,560+x), 2)
    # Bottom
    pygame.draw.line(screen, color, (40+x,560+x),(560+x,560+x), 2)
    # Bottom Right
    pygame.draw.line(screen, color, (560+x,560+x),(560+x,360+x), 2)
    pygame.draw.line(screen, color, (560+x,360+x),(520+x,360+x), 2)
    pygame.draw.line(screen, color, (520+x,360+x),(520+x,320+x), 2)
    pygame.draw.line(screen, color, (520+x,320+x),(760,320+x), 2)
    pygame.draw.line(screen, color, (760,280+x),(520+x,280+x), 2)
    pygame.draw.line(screen, color, (520+x,280+x),(520+x,240+x), 2)
    pygame.draw.line(screen, color, (520+x,240+x),(560+x,240+x), 2)
    pygame.draw.line(screen, color, (560+x,240+x),(560+x,40+x), 2)
    # Top Left Block
    pygame.draw.line(screen, color, (80+x,80+x),(80+x,200+x), 2)
    pygame.draw.line(screen, color, (80+x,200+x),(120+x,200+x), 2)
    pygame.draw.line(screen, color, (120+x,200+x),(120+x,120+x), 2)
    pygame.draw.line(screen, color, (120+x,120+x),(200+x,120+x), 2)
    pygame.draw.line(screen, color, (200+x,120+x),(200+x,80+x), 2)
    pygame.draw.line(screen, color, (200+x,80+x),(80+x,80+x), 2)
    # Top Right Block
    pygame.draw.line(screen, color, (400+x,80+x),(520+x,80+x), 2)
    pygame.draw.line(screen, color, (520+x,80+x),(520+x,200+x), 2)
    pygame.draw.line(screen, color, (520+x,200+x),(480+x,200+x), 2)
    pygame.draw.line(screen, color, (480+x,200+x),(480+x,120+x), 2)
    pygame.draw.line(screen, color, (480+x,120+x),(400+x,120+x), 2)
    pygame.draw.line(screen, color, (400+x,120+x),(400+x,80+x), 2)
    # Bottom Left Block
    pygame.draw.line(screen, color, (80+x,400+x),(80+x,520+x), 2)
    pygame.draw.line(screen, color, (80+x,520+x),(200+x,520+x), 2)
    pygame.draw.line(screen, color, (200+x,520+x),(200+x,480+x), 2)
    pygame.draw.line(screen, color, (200+x,480+x),(120+x,480+x), 2)
    pygame.draw.line(screen, color, (120+x,480+x),(120+x,400+x), 2)
    pygame.draw.line(screen, color, (120+x,400+x),(80+x,400+x), 2)
    #Bottom Right Block
    pygame.draw.line(screen, color, (400+x,520+x),(520+x,520+x), 2)
    pygame.draw.line(screen, color, (520+x,520+x),(520+x,400+x), 2)
    pygame.draw.line(screen, color, (520+x,400+x),(480+x,400+x), 2)
    pygame.draw.line(screen, color, (480+x,400+x),(480+x,480+x), 2)
    pygame.draw.line(screen, color, (480+x,480+x),(400+x,480+x), 2)
    pygame.draw.line(screen, color, (400+x,480+x),(400+x,520+x), 2)
    # Low Middle Block
    pygame.draw.line(screen, color, (240+x,520+x),(360+x,520+x), 2)
    pygame.draw.line(screen, color, (360+x,520+x),(360+x,480+x), 2)
    pygame.draw.line(screen, color, (360+x,480+x),(240+x,480+x), 2)
    pygame.draw.line(screen, color, (240+x,480+x),(240+x,520+x), 2)
    # Bigger Low Middle Block
    pygame.draw.line(screen, color, (120+x,320+x),(200+x,320+x), 2)
    pygame.draw.line(screen, color, (200+x,320+x),(200+x,400+x), 2)
    pygame.draw.line(screen, color, (200+x,400+x),(400+x,400+x), 2)
    pygame.draw.line(screen, color, (400+x,400+x),(400+x,320+x), 2)
    pygame.draw.line(screen, color, (400+x,320+x),(480+x,320+x), 2)
    pygame.draw.line(screen, color, (480+x,320+x),(480+x,360+x), 2)
    pygame.draw.line(screen, color, (480+x,360+x),(440+x,360+x), 2)
    pygame.draw.line(screen, color, (440+x,360+x),(440+x,440+x), 2)
    pygame.draw.line(screen, color, (440+x,440+x),(160+x,440+x), 2)
    pygame.draw.line(screen, color, (160+x,440+x),(160+x,360+x), 2)
    pygame.draw.line(screen, color, (160+x,360+x),(120+x,360+x), 2)
    pygame.draw.line(screen, color, (120+x,360+x),(120+x,320+x), 2)
    # Ghost Spawn
    pygame.draw.line(screen, color, (240+x,280+x),(240+x,360+x), 2)
    pygame.draw.line(screen, color, (240+x,360+x),(360+x,360+x), 2)
    pygame.draw.line(screen, color, (360+x,360+x),(360+x,280+x), 2)
    pygame.draw.line(screen, color, (360+x,280+x),(240+x,280+x), 2)
    # Top Middle Trap
    pygame.draw.line(screen, color, (240+x,80+x),(240+x,240+x), 2)
    pygame.draw.line(screen, color, (240+x,240+x),(360+x,240+x), 2)
    pygame.draw.line(screen, color, (360+x,240+x),(360+x,80+x), 2)
    pygame.draw.line(screen, color, (360+x,80+x),(320+x,80+x), 2)
    pygame.draw.line(screen, color, (320+x,80+x),(320+x,200+x), 2)
    pygame.draw.line(screen, color, (320+x,200+x),(280+x,200+x), 2)
    pygame.draw.line(screen, color, (280+x,200+x),(280+x,80+x), 2)
    pygame.draw.line(screen, color, (280+x,80+x),(240+x,80+x), 2)
    # Upper Mid Left Thing
    pygame.draw.line(screen, color, (120+x,280+x),(200+x,280+x), 2)
    pygame.draw.line(screen, color, (200+x,280+x),(200+x,160+x), 2)
    pygame.draw.line(screen, color, (200+x,160+x),(160+x,160+x), 2)
    pygame.draw.line(screen, color, (160+x,160+x),(160+x,240+x), 2)
    pygame.draw.line(screen, color, (160+x,240+x),(120+x,240+x), 2)
    pygame.draw.line(screen, color, (120+x,240+x),(120+x,280+x), 2)
    # Upper Mid Right Thing
    pygame.draw.line(screen, color, (400+x,160+x),(400+x,280+x), 2)
    pygame.draw.line(screen, color, (400+x,280+x),(480+x,280+x), 2)
    pygame.draw.line(screen, color, (480+x,280+x),(480+x,240+x), 2)
    pygame.draw.line(screen, color, (480+x,240+x),(440+x,240+x), 2)
    pygame.draw.line(screen, color, (440+x,240+x),(440+x,160+x), 2)
    pygame.draw.line(screen, color, (440+x,160+x),(400+x,160+x), 2)
    

    
    
def all_cells_pacman_is_in(x, y):
    cell_len = 40
    
    list_of_cells = []
    
    # Adding extra row to top and left side
    row = (x + cell_len) // cell_len
    column = (y + cell_len) // cell_len
    
    list_of_cells.extend((row, column))
    
    
    
    
    # If pacman is centered in cell
    def is_centered_in_cell(x, y):
        cell_len = 40
        return (x % cell_len == cell_len/2) and (y % cell_len == cell_len/2)
    
    # If pacman is centered in cell on y axis
    def is_centered_y(y):
        cell_len = 40
        return (y % cell_len == cell_len/2)
    
    # If pacman is centered in cell on x axis
    def is_centered_x(x):
        cell_len = 40
        return (x % cell_len == cell_len/2)
    

    
    if not is_centered_in_cell(x, y):
        if is_centered_y(y):
            # Since the cell is 40, if the location of pacman is
            # less than 19 or greater than 19, we need to add the
            # adjacent cell the the list of cells pacman is in
            if (x + cell_len) % cell_len >= (cell_len / 2 + 1):
                list_of_cells.extend((row+1, column))
            
            elif (x + cell_len) % cell_len <= (cell_len / 2 - 1):
                list_of_cells.extend((row-1, column))
    
    
    
    if not is_centered_in_cell(x, y):
        if is_centered_x(x):
            # Since the cell is 40, if the location of pacman is
            # less than 19 or greater than 19, we need to add the
            # adjacent cell the the list of cells pacman is in
            if (y + cell_len) % cell_len >= (cell_len / 2 + 1):
                list_of_cells.extend((row, column+1))
            
            elif (y + cell_len) % cell_len <= (cell_len / 2 - 1):
                list_of_cells.extend((row, column-1))
    
    
    
    list_of_x_values = list_of_cells[::2]
    list_of_y_values = list_of_cells[1::2]
    
    output_list = []
    
    for index in range(len(list_of_x_values)):
        output_list.append((list_of_x_values[index], list_of_y_values[index]))
        
    return output_list
    
    
    
    

    
    
    
    
    
def where_is_pacman(x, y):
    cell_len = 40
    
    # Adding extra row to top and left side
    row = (x + cell_len) // cell_len
    column = (y + cell_len) // cell_len
    
    return (row, column)



def is_centered_in_cell(x, y):
    cell_len = 40
    return (x % cell_len == cell_len/2) and (y % cell_len == cell_len/2)   
    

def is_centered_y(y):
    cell_len = 40
    return (y % cell_len == cell_len/2)
    
    
def is_centered_x(x):
    cell_len = 40
    return (x % cell_len == cell_len/2)









pacman_movements = {
    # Column 4
    (4,4): {'can_up':False, 'can_down':True, 'can_left':False, 'can_right':True},
    (5,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (6,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (7,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (8,4): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (9,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (10,4): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (11,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (12,4): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (13,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (14,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (15,4): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (16,4): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':False},
    
    
    # Column 5
    (4,5): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (8,5): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (10,5): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (12,5): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (16,5): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 6
    (4,6): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (6,6): {'can_up':False, 'can_down':True, 'can_left':False, 'can_right':True},
    (7,6): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (8,6): {'can_up':True, 'can_down':True, 'can_left':True, 'can_right':False},
    (10,6): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (12,6): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':True},
    (13,6): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (14,6): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':False},
    (16,6): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 7
    (4,7): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (6,7): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (8,7): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (10,7): {'can_up':True, 'can_down':False, 'can_left':False, 'can_right':False},
    (12,7): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (14,7): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (16,7): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 8
    (4,8): {'can_up':True, 'can_down':False, 'can_left':False, 'can_right':True},
    (5,8): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (6,8): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':False},
    (8,8): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (12,8): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (14,8): {'can_up':True, 'can_down':False, 'can_left':False, 'can_right':True},
    (15,8): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (16,8): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':False},
    
    # Column 9
    (5,9): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (8,9): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':True},
    (9,9): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (10,9): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (11,9): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (12,9): {'can_up':True, 'can_down':True, 'can_left':True, 'can_right':False},
    (15,9): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 10
    (-2,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (-1,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (0,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (1,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (2,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (3,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (4,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (5,10): {'can_up':True, 'can_down':True, 'can_left':True, 'can_right':True},
    (6,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (7,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (8,10): {'can_up':True, 'can_down':True, 'can_left':True, 'can_right':False},
    (12,10): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':True},
    (13,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (14,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (15,10): {'can_up':True, 'can_down':True, 'can_left':True, 'can_right':True},
    (16,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (17,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (18,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (19,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (20,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (21,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (22,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (23,10): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    
    
    # Column 11
    (5,11): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (8,11): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (12,11): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (15,11): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 12
    (4,12): {'can_up':False, 'can_down':True, 'can_left':False, 'can_right':True},
    (5,12): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':True},
    (6,12): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':False},
    (8,12): {'can_up':True, 'can_down':False, 'can_left':False, 'can_right':True},
    (9,12): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (10,12): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (11,12): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (12,12): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':False},
    (14,12): {'can_up':False, 'can_down':True, 'can_left':False, 'can_right':True},
    (15,12): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':True},
    (16,12): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':False},
    
    # Column 13
    (4,13): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (6,13): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (14,13): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (16,13): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    
    # Column 14
    (4,14): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (6,14): {'can_up':True, 'can_down':False, 'can_left':False, 'can_right':True},
    (7,14): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (8,14): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (9,14): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (10,14): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (11,14): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (12,14): {'can_up':False, 'can_down':True, 'can_left':True, 'can_right':True},
    (13,14): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (14,14): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':False},
    (16,14): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 15
    (4,15): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (8,15): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (12,15): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    (16,15): {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False},
    
    # Column 16
    (4,16): {'can_up':True, 'can_down':False, 'can_left':False, 'can_right':True},
    (5,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (6,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (7,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (8,16): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':True},
    (9,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (10,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (11,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (12,16): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':True},
    (13,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (14,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (15,16): {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True},
    (16,16): {'can_up':True, 'can_down':False, 'can_left':True, 'can_right':False},

}    
    
defined_cells = pacman_movements.keys()    
dots = []
for cell in defined_cells:
    dots.append(cell)
    
def draw_dot(cell):
    cell_len = 40
    coordinate = (cell * cell_len - cell_len) + (cell_len / 2)
    
    return coordinate

dot_image = pygame.image.load('dot.png')

    
def where_can_pacman_move(x, y):
    vertical = {'can_up':True, 'can_down':True, 'can_left':False, 'can_right':False}
    horizontal = {'can_up':False, 'can_down':False, 'can_left':True, 'can_right':True}
    
    if is_centered_in_cell(x, y):
        return pacman_movements[where_is_pacman(x, y)]
    else:
        if pacdirection == 4 or pacdirection == 2:
            return horizontal
            
        elif pacdirection == 1 or pacdirection == 3:
            return vertical
    


def shutdowngame():
    pygame.quit()

    
ghostchar = [pygame.image.load('ghost0.png'), pygame.image.load('ghost1.png')]
ghostchar_rot = []
ghosts = []
ghostx = []
ghosty = []
ghostcell = []
affected = []
ghostcolor = []
ghostdirection = []
previousdirection = []
state = []
ghosttype = []
turncooldown = []
deathanimation = 0
collidedghost = 0

def ghostsreset():
    ghostchar = [pygame.image.load('ghost0.png'), pygame.image.load('ghost1.png')]
    ghostchar_rot = []
    ghosts = []
    ghostx = []
    ghosty = []
    previousdirection = []
    ghostcolor = []
    ghostdirection = []
    affected = []
    state = []
    ghosttype = []
    turncooldown = []
    deathanimation = 0

    
def spawn_ghost(id,pos,color,gtype):
    ghostchar_rot.append(ghostchar)
    ghosts.append(id)
    ghostx.append(pos[0])
    ghosty.append(pos[1])
    ghostcell.append(all_cells_pacman_is_in(pos[0],pos[1]))
    ghostcolor.append(color)
    ghostdirection.append(randint(1,4))
    previousdirection.append("up")
    state.append(1)
    affected.append(0)
    ghosttype.append(gtype)
    turncooldown.append(1)
    
def recolor(img, oldcolor, newcolor):
    recolored = pygame.Surface(img.get_size())
    recolored.fill(newcolor)
    img.set_colorkey(oldcolor)
    recolored.blit(img, (0,0))
    return recolored

rshift_antirepeat = False

def redraw_window():
        global dots, score, ghostweak, ghostweaktime, pacman_lives, level
        map_color = (rgb[0],rgb[1],rgb[2])
        screen.blit(BG, (0,0))
        screen.blit(banner, (275,15))
        # Showing how many lives at the bottom with pacman animation
        if pacman_lives == 3:
            screen.blit(pacchar[1], (300, 700))
            screen.blit(pacchar[1], (360, 700))
            screen.blit(pacchar[1], (420, 700))
        if pacman_lives == 2:
            screen.blit(pacchar[1], (300, 700))
            screen.blit(pacchar[1], (360, 700))
        if pacman_lives == 1:
            screen.blit(pacchar[1], (360, 700))
        if pacman_lives == 0:
            game_over_sign = main_font.render('GAME OVER', 3, (255,255,255))
            finalscore_over_sign = main_font.render(f'Final Score: {score}', 3, (255,255,255))
            screen.blit(game_over_sign, (310, 320))
            screen.blit(finalscore_over_sign, (300, 360))
            global running
            pygame.display.update()
            fpsClock.tick(tickrate)
            running = False
            time.sleep(5000)
            pygame.time.wait(5000)

            
                            
            
        # Drawing dots / power ups
        if is_centered_in_cell(pacpos[0],pacpos[1]):
            newdotslist = []
            corner_power_ups = [(4,4), (4,16), (16,4), (16,16)]
            for dot in dots:
                if not dot == where_is_pacman(pacpos[0], pacpos[1]):
                    newdotslist.append(dot)
                else:
                    if dot in corner_power_ups:
                        score += 50
                        pygame.mixer.Sound.play(eat_powerup_sound)
                        ghostweak = ghostweaktime
                    else:
                        if dot != (10,14):
                            pygame.mixer.Sound.play(eat_pellet_sound)
                        score += 10
            dots = newdotslist
            
            #print(str(dots))
            #print(len(dots))
            
            if len(dots) <= 6:
                level += 1
                spawn_ghost(len(ghosts)+1,[380, 460],(randint(0,255),randint(0,255),randint(0,255)),"dumb")
                defined_cells = pacman_movements.keys()
                dots = []
                for cell in defined_cells:
                    dots.append(cell)

            
            
        radius = 7
        for dot in dots:
            corner_power_ups = [(4,4), (4,16), (16,4), (16,16)]
            x = draw_dot(int(dot[0]))
            y = draw_dot(int(dot[1]))
            if dot in corner_power_ups:
                #pygame.draw.circle(screen, (255,255,255), (x, y), radius)
                pygame.draw.circle(screen, (255,255,255), (int(x), int(y)), radius)
            else:
                screen.blit(dot_image, (x-4, y-4))
        # Rendering fonts for variables
        lives_label = main_font.render(f'Lives: {pacman_lives}', 1, (255,255,255))
        score_label = main_font.render(f'Score: {score}', 1, (255,255,255))
        level_label = main_font.render(f'Level: {level}', 1, (255,255,255))
        coordinates = main_font.render(f'Co: {pacpos[0]} {pacpos[1]}', 1, (255,255,255))
        where_is_pac = main_font.render(f'Cell: {where_is_pacman(pacpos[0], pacpos[1])}', 1, (255,255,255))
        is_pac_centered = main_font.render(f'Centered? {is_centered_in_cell(pacpos[0], pacpos[1])}', 1, (255,255,255))
        is_centered_on_x_coordinate = main_font.render(f'C on X? {is_centered_x(pacpos[0])}', 1, (255,255,255))
        is_centered_on_y_coordinate = main_font.render(f'C on Y? {is_centered_y(pacpos[1])}', 1, (255,255,255))
        cells_pac_is_in = main_font.render(f'ALL CELLS: {all_cells_pacman_is_in(pacpos[0], pacpos[1])}', 1, (255,255,255))
        
        # Where on the screen will the data be
        screen.blit(lives_label, (10,10))
        screen.blit(level_label, (130, 710))
        screen.blit(score_label, (540, 710))
        if debug_info == 1:
            screen.blit(coordinates, (175,10))
            screen.blit(where_is_pac, (410, 10))
            screen.blit(is_pac_centered, (200,200))
            screen.blit(is_centered_on_y_coordinate, (400,400))
            screen.blit(is_centered_on_x_coordinate, (200,600))
            screen.blit(cells_pac_is_in, (200,700))
        
        
        # Drawing pacman and hitbox
        radius = 20
        #pygame.draw.circle(screen, (255,255,0), (pacpos[0], pacpos[1]), radius)
        
        if debug_info == 1:
            pygame.draw.rect(screen, (255, 255, 0), (pacpos[0]-radius, pacpos[1]-radius, radius*2, radius*2), 2)
        
        #Draw map
        #draw_map(map_color)
        
        #pygame.display.update()
        

BG = pygame.transform.scale((pygame.image.load('background-black.png')), (screensize[0], screensize[1]))
banner = pygame.image.load('banner.png')

all_joysticks = initializeJoysticks()

gamestate = 0
ghostsspawned = 0

while running:
    
    ghostweak -= 1
    
    if ghostsspawned == 0:
        spawn_ghost(len(ghosts)+1,[380, 340],(255,0,0),"dumb")
        spawn_ghost(len(ghosts)+1,[380, 460],(252,177,3),"dumb")
        spawn_ghost(len(ghosts)+1,[340, 460],(252,189,247),"dumb")
        spawn_ghost(len(ghosts)+1,[420, 460],(39,238,245),"dumb")
        if level >= 2:
            for i in range(1,level-1):
                spawn_ghost(len(ghosts)+1,[380, 460],(randint(0,255),randint(0,255),randint(0,255)),"dumb")
        ghostsspawned = 1
        
    if pacmanmoving == 1 and gamestate == 0:
        gamestate = 1

        
    rgbcyclepos += 1
    if rgbcyclepos == 361:
        rgbcyclepos = 0
    if 60 > rgbcyclepos >= 0:
        rgb[1] += 4
    if 120 > rgbcyclepos >= 60:
        rgb[0] -= 4
    if 180 > rgbcyclepos >= 120:
        rgb[2] += 4
    if 240 > rgbcyclepos >= 180:
        rgb[1] -= 4
    if 300 > rgbcyclepos >= 240:
        rgb[0] += 4
    if 360 > rgbcyclepos >= 300:
        rgb[2] -= 4
    #print(rgb)
    screen.fill(background_color)
    redraw_window()
    pygame.mouse.set_visible(False)
    pygame.event.get()    
    keys=pygame.key.get_pressed()
    
    #statstext = "{} {} ({}x{}) [{}] {}({}) {} ({}, {}) {} ({}) [{}, {}, {}] ".format(int(pacpos[0]),int(pacpos[1]),screensize[0],screensize[1],tickrate,pacman_speed,shift_multiplier,ghost_speed,speed_increments[0],speed_increments[1],powerup_time,powerup_decrement,resets[0],resets[1],resets[2])
    #statsdisp = font.render(statstext, False, (255, 255, 255))
    
    
        
    if keys[K_ESCAPE]:
        running = False
        
    movement = where_can_pacman_move(pacpos[0], pacpos[1])
        
    
    if keys[K_RSHIFT]: ## Spawns a 'dumb' ghost with random color at a random position
        if not rshift_antirepeat:
            spawn_ghost(len(ghosts)+1,ghost_spawn,(randint(0,255), randint(0,255), randint(0,255)),"dumb")
            rshift_antirepeat = True
    else:
        rshift_antirepeat = False
        
    if running == False:
            shutdowngame()
            
    if not (len(joysticks) == 0 ):
        joystickpos = [pygame.joystick.Joystick(0).get_axis(0),pygame.joystick.Joystick(0).get_axis(1)]
        joystickmovements = [False,False,False,False]
        #Up, Down, Left, Right
        
        if joystickpos[0] >= joystick_threshold:
            joystickmovements[3] = True
        if joystickpos[0] <= (joystick_threshold*-1):
            joystickmovements[2] = True
        if joystickpos[1] >= joystick_threshold:
            joystickmovements[1] = True
        if joystickpos[1] <= (joystick_threshold*-1):
            joystickmovements[0] = True
        
    #print(str(joystickmovements))
    
    if keys[K_UP] and movement['can_up']:
    #if keys[K_UP]:
        pacmanmoving = True
        pacdirection = 1
    elif keys[K_RIGHT] and movement['can_right']:
    #elif keys[K_RIGHT]:
        pacmanmoving = True
        pacdirection = 2
    elif keys[K_DOWN] and movement['can_down']:
    #elif keys[K_DOWN]:
        pacmanmoving = True
        pacdirection = 3
    elif keys[K_LEFT] and movement['can_left']:
    #elif keys[K_LEFT]:
        pacmanmoving = True
        pacdirection = 4
    elif not (len(joysticks) == 0):
        if joystickmovements[0] and movement['can_up']:
        #if keys[K_UP]:
            pacmanmoving = True
            pacdirection = 1
        elif joystickmovements[3] and movement['can_right']:
        #elif keys[K_RIGHT]:
            pacmanmoving = True
            pacdirection = 2
        elif joystickmovements[1] and movement['can_down']:
        #elif keys[K_DOWN]:
            pacmanmoving = True
            pacdirection = 3
        elif joystickmovements[2] and movement['can_left']:
        #elif keys[K_LEFT]:
            pacmanmoving = True
            pacdirection = 4
    
    
    
    
    if keys[K_LSHIFT]:
        pacman_newspeed = pacman_speed
    else:
        pacman_newspeed = pacman_speed
        
    #print(str(pygame.joystick.Joystick(0).get_axis(0)))
        
    if pacmanmoving == True:
        if pacdirection == 1 and not movement['can_up']:
            pacmanmoving = False
            pacdirection = 0
        if pacdirection == 2 and not movement['can_right']:
            pacmanmoving = False
            pacdirection = 0
        if pacdirection == 3 and not movement['can_down']:
            pacmanmoving = False
            pacdirection = 0
        if pacdirection == 4 and not movement['can_left']:
            pacmanmoving = False
            pacdirection = 0
            
        pacanim += 1
        if pacanim >= 9:
            pacanim = 0
        if pacdirection == 1:
            pacpos[1] -= pacman_newspeed
            pacman = pygame.transform.rotate(pacchar[pacanim//3], 90)
        elif pacdirection == 2:
            pacpos[0] += pacman_newspeed
            pacman = pygame.transform.rotate(pacchar[pacanim//3], 0)
        elif pacdirection == 3:
            pacpos[1] += pacman_newspeed
            pacman = pygame.transform.rotate(pacchar[pacanim//3], 270)
        elif pacdirection == 4:
            pacpos[0] -= pacman_newspeed
            pacman = pygame.transform.rotate(pacchar[pacanim//3], 180)
    if pacmanmoving == False:
        pacanim = 0
        pacman = pygame.transform.rotate(pacchar[pacanim//3], 0)
    
    ghostanim += 1
    if ghostanim >= 9:
        ghostanim = 0
    
    
    for i in range(0,len(ghosts)):
        if len(ghosts) >= 1:
            if abs(ghostx[i] - pacpos[0]) < hitbox:
                if abs(ghosty[i] - pacpos[1]) < hitbox:
                    if affected[i] == 1:
                        affected[i] = 2
                        pygame.mixer.Sound.play(eat_powerup_sound)
                        score += 250
                    elif affected[i] == 2:
                        ghostx[i] = 380
                        ghosty[i] = 460
                    else:
                        deathanimation = 300
                        collidedghost = i
        ghostcell[i] = all_cells_pacman_is_in(ghostx[i],ghosty[i])
        #print(ghostcell[i])
              
        if ghostx[i] <= -40:
            ghostx[i] += screensize[0]+40
        if ghostx[i] >= screensize[0]:
            ghostx[i] -= screensize[0]+40
        if ghosty[i] <= -40:
            ghosty[i] += screensize[1]+40
        if ghosty[i] >= screensize[1]:
            ghosty[i] -= screensize[1]+40
        turncooldown[i] -= 1
        
        if ghostweak == ghostweaktime:
            affected[i] = 1
        if ghostweak == 0:
            affected[i] = 0
        if affected[i] == 2:
            ghostx[i] = 380
            ghosty[i] = 460
                            
        ghostmovess = pacman_movements[where_is_pacman(ghostx[i], ghosty[i])]
        
        if ghostdirection[i] == 1:
            previousdirection[i] = "up"
            turncooldown[i] = 0
        if ghostdirection[i] == 2:
            previousdirection[i] = "right"
            turncooldown[i] = 0
        if ghostdirection[i] == 3:
            previousdirection[i] = "down"
            turncooldown[i] = 0
        if ghostdirection[i] == 4:
            previousdirection[i] = "left"
            turncooldown[i] = 0
            
    
        if turncooldown[i] <= 0:
            if ghosttype[i] == "dumb":
                if is_centered_in_cell(ghostx[i], ghosty[i]):
                    #print(ghostcell[i])
                    ghostmovements = pacman_movements[where_is_pacman(ghostx[i], ghosty[i])]
                    ghostmoves = []
                    if ghostmovements['can_right'] and not previousdirection[i] == "left":
                        ghostmoves = ghostmoves + ["right"]
                    if ghostmovements['can_left'] and not previousdirection[i] == "right":
                        ghostmoves = ghostmoves + ["left"]
                    if ghostmovements['can_up'] and not previousdirection[i] == "down":
                        ghostmoves = ghostmoves + ["up"]
                    if ghostmovements['can_down'] and not previousdirection[i] == "up":
                        ghostmoves = ghostmoves + ["down"]
                        
                    if len(ghostmoves) == 0:
                        chosendirection = "up"
                    else:
                        chosendirection = ghostmoves[randint(0,len(ghostmoves)-1)]
                    
                    if chosendirection == "right":
                        ghostdirection[i] = 2
                    if chosendirection == "up":
                        ghostdirection[i] = 1
                    if chosendirection == "down":
                        ghostdirection[i] = 3
                    if chosendirection == "left":
                        ghostdirection[i] = 4
                    #print(previousdirection[i] + " --> " + chosendirection)
                        #turncooldown[i] = randint(15,300)
                    turncooldown[i] = 1
            elif ghosttype[i] == "smart":
                if is_centered_in_cell(ghostx[i], ghosty[i]):
                    #print(ghostcell[i])
                    ghostmovements = pacman_movements[where_is_pacman(ghostx[i], ghosty[i])]
                    ghostmoves = []
                    if ghostmovements['can_right']:
                        ghostmoves = ghostmoves + ["right"]
                    if ghostmovements['can_left']:
                        ghostmoves = ghostmoves + ["left"]
                    if ghostmovements['can_up']:
                        ghostmoves = ghostmoves + ["up"]
                    if ghostmovements['can_down']:
                        ghostmoves = ghostmoves + ["down"]
                        
                    if len(ghostmoves) == 0:
                        chosendirection = "up"
                    else:
                        needtogo = []
                        if ghostx[i] >= pacpos[0]:
                            needtogo = needtogo + ["left"]
                        else:
                            needtogo = needtogo + ["right"]
                        if ghosty[i] >= pacpos[1]:
                            needtogo = needtogo + ["up"]
                        else:
                            needtogo = needtogo + ["down"]
                            
                        cango = []
                        for i in range(0,len(needtogo)-1):
                            for x in range(0,len(ghostmoves)-1):
                                if ghostmoves[x] == needtogo[i]:
                                    cango = cango + [ghostmoves[x]]
                        
                        if len(cango) >= 1:
                            chosendirection = cango[randint(0,len(cango)-1)]
                        else:
                            chosendirection = ghostmoves[randint(0,len(ghostmoves)-1)]
                            
                            
                            
                    if chosendirection == "right":
                        ghostdirection[i] = 2
                    if chosendirection == "up":
                        ghostdirection[i] = 1
                    if chosendirection == "down":
                        ghostdirection[i] = 3
                    if chosendirection == "left":
                        ghostdirection[i] = 4
                    #print(previousdirection[i] + " --> " + chosendirection)
                        #turncooldown[i] = randint(15,300)
                    turncooldown[i] = 1
                    
                    
                    
                    
        if gamestate == 1 and ghostdirection[i] == 1:
            ghosty[i] -= ghost_speed
            ghostchar_rot[i] = pygame.transform.flip(ghostchar[ghostanim//5], True, False)
        elif gamestate == 1 and ghostdirection[i] == 2:
            ghostx[i] += ghost_speed
            ghostchar_rot[i] = pygame.transform.flip(ghostchar[ghostanim//5], True, False)
        elif gamestate == 1 and ghostdirection[i] == 3:
            ghosty[i] += ghost_speed
            ghostchar_rot[i] = ghostchar[ghostanim//5]
        elif gamestate == 1 and ghostdirection[i] == 4:
            ghostx[i] -= ghost_speed
            ghostchar_rot[i] = ghostchar[ghostanim//5]
        else:
            ghostchar_rot[i] = ghostchar[ghostanim//5]
            
        if affected[i] == 1:
            if ghostweak >= 90:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (0,0,200)).convert()
            elif 90 > ghostweak >= 75:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (0,0,200)).convert()
            elif 75 > ghostweak >= 50:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (255,255,255)).convert()
            elif 50 > ghostweak >= 35:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (0,0,200)).convert()
            elif 35 > ghostweak >= 25:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (255,255,255)).convert()
            elif 25 > ghostweak > 15:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (0,0,200)).convert()
            elif 15 > ghostweak >= 5:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (255,255,255)).convert()
            elif 5 > ghostweak > 0:
                ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (0,0,200)).convert()
                
        elif affected[i] == 2:
            ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), (0,0,0)).convert()
        else:
            ghostchar_rot[i] = recolor(ghostchar_rot[i], (29, 184, 235), ghostcolor[i]).convert()   
            
        ghostchar_rot[i].set_colorkey((0,0,0))
        
        
        screen.blit(ghostchar_rot[i], (ghostx[i]-20, ghosty[i]-20))
    
    screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
    
    if pacpos[0] <= -40:
        pacpos[0] += screensize[0]+40
    if pacpos[0] >= screensize[0]:
        pacpos[0] -= screensize[0]+40
    if pacpos[1] <= -40:
        pacpos[1] += screensize[1]+40
    if pacpos[1] >= screensize[1]:
        pacpos[1] -= screensize[1]+40

    #Everything below this has to be ran at the end of the while loop
    
    draw_map((rgb[0],rgb[1],rgb[2]))
    
    while start_time >= 1:
        screen.fill(background_color)
        screen.blit(pacman, (360, 520))
        if debug_info == 1:
            screen.blit(statsdisp, (0, 0))
        countdowntext = "Starting in {}..".format(start_time-1)
        cddisplay = font.render(countdowntext, 2, (255, 255, 255))
        screen.blit(cddisplay, (315, 320))
        pygame.display.update()
        fpsClock.tick(tickrate)
        pygame.time.wait(1000)
        start_time -= 1
        
    while deathanimation > 1:
        if deathanimation == 300:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(death_sound)
        if 300 >= deathanimation >= 240:
            screen.fill(background_color)
            ghostchar_rot[collidedghost] = recolor(ghostchar_rot[collidedghost], (29, 184, 235), ghostcolor[collidedghost]).convert()
            ghostchar_rot[collidedghost].set_colorkey((0,0,0))
            screen.blit(ghostchar_rot[collidedghost], (ghostx[collidedghost]-20, ghosty[collidedghost]-20))
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 240 > deathanimation >= 220:
            ghostchar_rot = []
            ghosts = []
            ghostx = []
            ghosty = []
            ghostcolor = []
            ghostdirection = []
            state = []
            ghosttype = []
            turncooldown = []
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 90)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 220 > deathanimation >= 200:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 180)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 200 > deathanimation >= 180:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 270)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 180 > deathanimation >= 160:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 0)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 160 > deathanimation >= 140:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 90)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 140 > deathanimation >= 120:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 180)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 120 > deathanimation >= 100:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 270)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 100 > deathanimation >= 80:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 0)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))
        elif 80 > deathanimation >= 60:
            screen.fill(background_color)
            pacman = pygame.transform.rotate(pacchar[2], 90)
            screen.blit(pacman, (pacpos[0]-20,pacpos[1]-20))   
        elif deathanimation <= 2:
            pacpos[0] = 380
            pacpos[1] = 540
            pacdirection = 0
            pacanim = 0
            pacman_lives -= 1
            pygame.mixer.music.play()
            pacmanmoving = False
            ghostsspawned = 0
            gamestate = 0
            
            
        pygame.display.update()
        fpsClock.tick(tickrate)
        deathanimation -= 2
        
        
        
    if debug_info == 1:
        screen.blit(statsdisp, (0, 0))
    pygame.display.update()
    fpsClock.tick(tickrate)


# In[ ]:





# In[ ]:





# In[ ]:




