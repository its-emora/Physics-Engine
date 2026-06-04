import pygame
import pygame_textinput
import random as r
import math as m
import block_class

pygame.init()

airres_input = pygame_textinput.TextInputVisualizer()
friction_input = pygame_textinput.TextInputVisualizer()
restitution_input = pygame_textinput.TextInputVisualizer()
velocity_input = pygame_textinput.TextInputVisualizer()
angle_input = pygame_textinput.TextInputVisualizer()


# Bools
velocity_input_selected = False
angle_input_selected = False
airres_input_selected = False
rest_input_selected = False
fric_input_selected = False
# Pygame
vector = pygame.math.Vector2
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
# Groups
blocks_group = pygame.sprite.Group()
# Arrays
block_textures = ["blue_block","red_block"]
# Colours
WHITE = (200,200,200)
BLACK = (20,20,20)
# Text
font = pygame.font.Font("Blocks/assets/fonts/menu_font.ttf",24)
velocity_text = font.render("Initial Velocity:", True, BLACK)
vel_rect = velocity_text.get_rect(topleft=(25,100))
angle_text = font.render("Angle of fire:", True, BLACK)
ang_rect = angle_text.get_rect(topleft=(25,125))
restitution_text = font.render("Coefficient of Restitution:",True, BLACK)
rest_rect = restitution_text.get_rect(topleft=(25,75))
friction_text = font.render("Coefficient of Friction (Ground):", True, BLACK)
fric_rect = friction_text.get_rect(topleft=(25,50))
air_resistance_text = font.render("Coefficient of Friction (Air):", True, BLACK)
air_res_rect = friction_text.get_rect(topleft=(25,25))

root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
fire = False

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            velocity_input_selected, angle_input_selected, airres_input_selected, fric_input_selected, rest_input_selected = False,False,False,False,False
            if vel_rect.collidepoint(event.pos):
                velocity_input_selected = True
            elif ang_rect.collidepoint(event.pos):
                angle_input_selected = True
            elif air_res_rect.collidepoint(event.pos):
                airres_input_selected = True
            elif rest_rect.collidepoint(event.pos):
                rest_input_selected = True
            elif fric_rect.collidepoint(event.pos):
                fric_input_selected = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f and not velocity_input_selected and not angle_input_selected:
                fire = True
                try:
                    block = block_class.BLOCK(float(velocity_input.value),float(angle_input.value),
                                  float(restitution_input.value),float(friction_input.value),float(airres_input.value))
                    blocks_group.add(block)
                except:
                    pass
            if event.key == pygame.K_DELETE:
                for block in blocks_group:
                    blocks_group.remove(block)

    delta_time = clock.tick(60)/1000

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    root.fill(WHITE)

    velocity_input.cursor_visable = False

    if rest_input_selected:
        restitution_input.update(events)
    
    if fric_input_selected:
        friction_input.update(events)

    if airres_input_selected:
        airres_input.update(events)

    if velocity_input_selected:
        velocity_input.update(events)

    if angle_input_selected:
        angle_input.update(events)

    root.blit(air_resistance_text,air_res_rect)
    root.blit(friction_text,fric_rect)
    root.blit(restitution_text,rest_rect)    
    root.blit(velocity_text,vel_rect)
    root.blit(angle_text,ang_rect)
    root.blit(velocity_input.surface,(450,100))
    root.blit(angle_input.surface,(450,125))
    root.blit(restitution_input.surface,(450,75))
    root.blit(airres_input.surface,(450,25))
    root.blit(friction_input.surface,(450,50))

    if fire:
        blocks_group.update()
    blocks_group.draw(root)

    pygame.display.flip()

pygame.quit()