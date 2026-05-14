import pygame
import math
import random as r

pygame.init()

# Vectors:
vector = pygame.math.Vector2
# Groups
blocks_group = pygame.sprite.Group()
# Arrays
block_textures = ["blue_block","red_block"]
# Colours
WHITE = (255,255,255)

class BLOCK(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.colour = r.choice(block_textures)

        self.image = pygame.image.load(f"Blocks/assets/images/{self.colour}.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (x,y)

        self.grabbed = False

        self.position = vector(x,y)
        self.velocity = vector(r.randint(1,25),-r.randint(5,25))
        self.acceleration = vector(0,0)

        self.HORIZONTAL_ACCELERATION = 2
        self.FRICTION_COEFFICIENT = 0.2
        self.GRAVITATIONAL_CONSTANT = 0.5

    def update(self):
        self.acceleration = vector(0,self.GRAVITATIONAL_CONSTANT)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
        if keys[pygame.K_d]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION

        if self.position.y == 1080:
            self.FRICTION_COEFFICIENT = 0.05
        else:
            self.FRICTION_COEFFICIENT = 0

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

block = BLOCK(100,1080)
blocks_group.add(block)

fire = False

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
    
    if keys[pygame.K_f]:
        fire = True

    if fire:
        blocks_group.update()
    blocks_group.draw(root)

    pygame.display.flip()

pygame.quit()