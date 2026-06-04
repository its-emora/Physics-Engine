#---- IMPORTS ----#
import pygame
import math
import random

# Initilising
pygame.init()

# Defining window
root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

vector = pygame.math.Vector2
group = pygame.sprite.Group()

#---- CONSTANTS ----# 
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h

#---- SUB-ROUTINES ----#
def sim_coordinates(x,y):
    x += screen_width/2
    y += screen_height/2
    return x,y

def raw_coordinates(x,y):
    x -= screen_width/2
    y -= screen_height/2

# Defining main body
class MAIN_BODY(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pass

#---- GAME LOOP----#
run_loop = True
while run_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_loop = False
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_ESCAPE]:
        run_loop = False
        
pygame.quit()