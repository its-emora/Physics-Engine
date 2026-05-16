import pygame
import pygame_textinput
import random as r
import math as m

pygame.init()

velocity_input = pygame_textinput.TextInputVisualizer()
angle_input = pygame_textinput.TextInputVisualizer()

# Bools
velocity_input_selected = False
angle_input_selected = False
# Pygame
vector = pygame.math.Vector2
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
# Groupss
blocks_group = pygame.sprite.Group()
# Arrays
block_textures = ["blue_block","red_block"]
# Colours
WHITE = (200,200,200)
BLACK = (20,20,20)
# Text
font = pygame.font.Font("Blocks/assets/fonts/menu_font.ttf",24)
velocity_text = font.render("Velocity:", True, BLACK)
vel_rect = velocity_text.get_rect(topleft=(25,100))
angle_text = font.render("Angle:", True, BLACK)
ang_rect = angle_text.get_rect(topleft=(25,125))

class BLOCK(pygame.sprite.Sprite):
    def __init__(self,velocity,angle):
        super().__init__()
        self.colour = r.choice(block_textures)

        self.image = pygame.image.load(f"Blocks/assets/images/{self.colour}.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (55,1075)

        self.grabbed = False

        self.position = vector(50,1080)
        self.velocity = vector(velocity*m.cos(m.radians(angle)),-velocity*m.sin(m.radians(angle)))
        self.acceleration = vector(0,0)

        self.HORIZONTAL_ACCELERATION = 2
        self.FRICTION_COEFFICIENT = 0.08
        self.GRAVITATIONAL_CONSTANT = 0.5
        self.RESTITUTION_COEFFICIENT = -0.9


    def update(self):
        self.acceleration = vector(0,self.GRAVITATIONAL_CONSTANT)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
        if keys[pygame.K_d]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION

        if self.position.y >= screen_height:
            self.FRICTION_COEFFICIENT = 0.01
        else:
            self.FRICTION_COEFFICIENT = 0

        self.acceleration.x -= self.velocity.x * self.FRICTION_COEFFICIENT
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration / 2

        if self.position.y >= screen_height:
            self.position.y = screen_height
            self.velocity.y *= self.RESTITUTION_COEFFICIENT
        if self.position.y <= 64:
            self.position.y = 64
            self.velocity.y *= self.RESTITUTION_COEFFICIENT
        if self.position.x >= screen_width:
                self.position.x = screen_width
                self.velocity.x *= self.RESTITUTION_COEFFICIENT
        if self.position.x <= 64:
                self.position.x = 64
                self.velocity.x *= self.RESTITUTION_COEFFICIENT
        self.rect.bottomright = self.position

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
            if vel_rect.collidepoint(event.pos):
                velocity_input_selected = True
                angle_input_selected = False
            elif ang_rect.collidepoint(event.pos):
                angle_input_selected = True
                velocity_input_selected = False
            else:
                velocity_input_selected = False
                angle_input_selected = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f and not velocity_input_selected and not angle_input_selected:
                fire = True
                try:
                    block = BLOCK(float(velocity_input.value),float(angle_input.value))
                    blocks_group.add(block)
                except:
                    pass
            if event.key == pygame.K_RETURN:
                velocity_input_selected = False
                angle_input_selected = False
            if event.key == pygame.K_c:
                velocity_input_selected = False
                angle_input_selected = True
            if event.key == pygame.K_DELETE:
                for block in blocks_group:
                    blocks_group.remove(block)

    delta_time = clock.tick(60)/1000

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    root.fill(WHITE)

    velocity_input.cursor_visable = False

    if velocity_input_selected:
        velocity_input.update(events)

    if angle_input_selected:
        angle_input.update(events)

    root.blit(velocity_text,vel_rect)
    root.blit(angle_text,ang_rect)
    root.blit(velocity_input.surface,(130,100))
    root.blit(angle_input.surface,(130,125))

    if fire:
        blocks_group.update()
    blocks_group.draw(root)

    pygame.display.flip()

pygame.quit()