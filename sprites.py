from settings import *
import pygame as pg
from random import choice, randrange
from os import path
import time

vc = pg.math.Vector2

class Spritesheet:
    #utility for images
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()
    def bg(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        return image    
     
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = P_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.pos = vc(20, HEIGHT - 100)
        self.vel = vc(0,0)
        self.pos.x = 50
        self.pos.y = 300
        
    def update(self):
        self.animate()
        self.acc = vc(0,0.8)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos.x = 50
        if self.pos.y > HEIGHT - 100:
            self.pos.y = HEIGHT - 100
            self.vel.y = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vel.y = 0            
        self.rect.midbottom = self.pos
    def animate(self):
        if self.vel.y == 0:
            self.image = self.images[1]
        if self.vel.y > 0:
            self.image = self.images[0]
        if self.vel.y < 0:
            self.image = self.images[2]       
    def load_images(self):
        self.images = [self.game.spritesheet.bg(54,672,34,24),
             self.game.spritesheet.bg(36,994,34,24),
             self.game.spritesheet.bg(0,994,34,24)]
        for image in self.images:
            image.set_colorkey(BLACK)        
    def jump(self):
        self.vel.y = -PLAYER_JUMP
        

class Background(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = BACKGROUND_LAYER
        self.groups = game.all_sprites, game.backgrounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.bg(0,114,288,512)
        self.rect = self.image.get_rect()
class Ground(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.backgrounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.bg(0,0,336,112)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 100

class Pipes(pg.sprite.Sprite):
    def __init__(self, game, distance, y):
        self._layer = ENV_LAYER
        self.groups = game.all_sprites, game.pipes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game               
        self.image = self.game.spritesheet.bg(0,672,52,320)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = distance
  
class Pipes_up(pg.sprite.Sprite):
    def __init__(self, game, distance, y):
        self._layer = ENV_LAYER
        self.groups = game.all_sprites, game.pipes_up
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game               
        self.image = self.game.spritesheet.bg(0,672,52,320)
        self.image = pg.transform.flip(self.image, False, True)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y - 460
        self.rect.x = distance