import pygame
import random as r
import math as m

pygame.init()

vector = pygame.math.Vector2

block_textures = ["blue_block","red_block"]

display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h

class BLOCK(pygame.sprite.Sprite):
    def __init__(self,velocity,angle,restitution,f_surface,f_air):
        super().__init__()
        self.colour = r.choice(block_textures)

        self.image = pygame.image.load(f"Blocks/assets/images/{self.colour}.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (55,1075)

        self.grabbed = False

        self.position = vector(55,1075)
        self.velocity = vector(velocity*m.cos(m.radians(angle)),-velocity*m.sin(m.radians(angle)))
        self.acceleration = vector(0,0)

        self.FRICTION_COEFFICIENT_SURFACE = f_surface
        self.FRICTION_COEFFICIENT_AIR = f_air
        self.GRAVITATIONAL_CONSTANT = 0.5
        self.RESTITUTION_COEFFICIENT = restitution

    def update(self):
        self.acceleration = vector(0,self.GRAVITATIONAL_CONSTANT)

        if self.position.y >= screen_height:
            applied_friction = self.FRICTION_COEFFICIENT_SURFACE
        else:
            applied_friction = self.FRICTION_COEFFICIENT_AIR

        self.acceleration.x -= self.velocity.x * applied_friction
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration / 2

        if self.position.y >= screen_height:
            self.position.y = screen_height
            self.velocity.y *= -1*self.RESTITUTION_COEFFICIENT
        if self.position.y <= 64:
            self.position.y = 64
            self.velocity.y *= -1*self.RESTITUTION_COEFFICIENT
        if self.position.x >= screen_width:
                self.position.x = screen_width
                self.velocity.x *= -1*self.RESTITUTION_COEFFICIENT
        if self.position.x <= 64:
                self.position.x = 64
                self.velocity.x *= -1*self.RESTITUTION_COEFFICIENT
                
        self.rect.bottomright = self.position