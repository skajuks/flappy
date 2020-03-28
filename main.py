from settings import *
import pygame as pg
import math, random, sys
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.MAINWINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(gameTitle)
        self.load_data()
        self.running = True

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def update(self):
        self.all_sprites.update()
        pg.display.set_caption(gameTitle + ' ' + str(round(self.clock.get_fps(), 1)))
        hits1 = pg.sprite.spritecollide(self.player, self.pipes, False)
        hits2 = pg.sprite.spritecollide(self.player, self.pipes_up, False)
        if (hits1 or hits2) or self.player.pos.y >= HEIGHT - 100:
            print('game over')
            self.hit_sound.play()
            self.playing = False             
        for pipe in self.pipes:
            pipe.rect.x -=3            
            if pipe.rect.right <= 0:
                pipe.kill()
            if pipe.rect.right < 100 and pipe.rect.right > 96 :    
                self.spawn = True
            if (pipe.rect.right < WIDTH) and self.spawn == True:
                Pipes(self, WIDTH + 200, random.randrange(HEIGHT-  360, HEIGHT - 120))
                for pipe in self.pipes:                   
                    Pipes_up(self, pipe.rect.x, pipe.rect.top)
                self.spawn = False
        for pipe in self.pipes_up:
            pipe.rect.x -=3
            if pipe.rect.right <= 0:
                pipe.kill()
        while len(self.pipes) < 1:       
            Pipes(self, WIDTH, random.randrange(HEIGHT-  360, HEIGHT - 120))      
            for pipe in self.pipes:                   
                Pipes_up(self, pipe.rect.x, pipe.rect.top)
    def new(self):
        self.jump = True  
        self.spawn = True
        self.game = True
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.backgrounds = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.pipes_up = pg.sprite.Group()
        self.player = Player(self)
        Background(self)
        Ground(self)
        self.player.jump()
        g.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False    
            if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE and self.jump == True:
                   self.player.jump()
                   self.wing_sound.play()
            if event.type == pg.MOUSEBUTTONDOWN and self.jump == True:
                self.player.jump() 
                self.wing_sound.play()  
    def draw(self):
        self.MAINWINDOW.fill(BLACK)
        self.all_sprites.draw(self.MAINWINDOW)
        pg.display.flip()       
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'textures')

        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITES))

        self.sound_dir = path.join(self.dir, 'sound')
        self.wing_sound = pg.mixer.Sound(path.join(self.sound_dir, 'wing.wav'))
        self.hit_sound = pg.mixer.Sound(path.join(self.sound_dir, 'hit.wav'))
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
