import pygame
import math
import random

pygame.init()


# ---- VARIABLES ---- #
# ---- Constants:
# Colours:
BLACK = (0,0,0)
DARKGREY = (75,75,75)
GREY = (165,165,165)
LIGHTGREY = (200,200,200)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (165,0,165)
# Vectors:
vector = pygame.math.Vector2
# Groups
blocks_group = pygame.sprite.Group()
# Arrays
block_textures = ["blue_block","red_block"]

# ---- CLASSES ---- #
class BLOCK(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.colour = random.choice(block_textures)

        self.image = pygame.image.load(f"Blocks/assets/images/{self.colour}.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (x,y)

        self.grabbed = False

        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)

        self.HORIZONTAL_ACCELERATION = 1
        self.FRICTION_COEFFICIENT = 0.1
        self.GRAVITATIONAL_CONSTANT = 0.5

    def update(self):
        grabbed = False
        possible_grabbed = False

        mouse_pos = pygame.mouse.get_pos()
        self.acceleration = vector(0,0)
        
        if self.position.x-64 > mouse_pos[0] > self.position.x and self.position.y-64 > mouse_pos[1] > self.position.y:
            possible_grabbed = False
            if not mouse_pressed[0]:
                grabbed = False
        else:
            possible_grabbed = True
            if mouse_pressed[0] and possible_grabbed:
                self.position = vector(mouse_pos[0]+32,mouse_pos[1]+32)
                self.velocity = vector(0,0)
                grabbed = True
            

        if not grabbed:
            self.acceleration = vector(0,self.GRAVITATIONAL_CONSTANT)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            if keys[pygame.K_d]:
                self.acceleration.x = self.HORIZONTAL_ACCELERATION

            self.acceleration.x -= self.velocity.x * self.FRICTION_COEFFICIENT
            self.velocity += self.acceleration
            self.position += self.velocity + self.acceleration / 2

            if self.position.y >= 1080:
                self.position.y = 1080

            if self.position.x > 1984 or self.position.x < 0:
                blocks_group.remove(self)
                    
        self.rect.bottomright = self.position


root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

block = BLOCK(1000,500)
blocks_group.add(block)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s:
                blocks_group.add(BLOCK(mouse_pos[0],mouse_pos[1]))

    delta_time = clock.tick(60)/1000

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    root.fill(WHITE)

    blocks_group.update()
    blocks_group.draw(root)

    pygame.display.flip()

pygame.quit()