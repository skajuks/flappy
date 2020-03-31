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
        self.font_name = pg.font.match_font(FONT_NAME)

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
        hits1 = pg.sprite.spritecollide(self.player, self.pipes, False, pg.sprite.collide_mask)
        hits2 = pg.sprite.spritecollide(self.player, self.pipes_up, False, pg.sprite.collide_mask)
        if (hits1 or hits2) or self.player.pos.y >= HEIGHT - 100:
            print('game over')
            self.hit_sound.play()
            self.playing = False             
        for pipe in self.pipes:
            pipe.rect.x -=3 
            if self.player.rect.centerx > pipe.rect.centerx - 2 and self.player.rect.centerx < pipe.rect.centerx + 2 :
                self.score +=1           
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
        self.score = 0
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
        self.draw_text(str(self.score), 40, WHITE, WIDTH // 2, 15)
        pg.display.flip()
              
    def show_start_screen(self):
        self.draw_text("Press any key to play again" ,14, WHITE, WIDTH // 2, HEIGHT  // 2)   
        pg.display.flip()
        self.waitForKey()
    def show_go_screen(self):
        if not self.running:
            return
        self.draw_text("Score : " + str(self.score) ,22 ,WHITE, WIDTH // 2 , HEIGHT // 3)
        self.draw_text("Press any key to play again" ,14, WHITE, WIDTH // 2, HEIGHT  // 2)   
        self.image = self.spritesheet.bg(0,628,192,42)
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 4
        self.MAINWINDOW.blit(self.image, self.rect)
        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False
    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'textures')

        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITES))

        self.sound_dir = path.join(self.dir, 'sound')
        self.wing_sound = pg.mixer.Sound(path.join(self.sound_dir, 'wing.wav'))
        self.hit_sound = pg.mixer.Sound(path.join(self.sound_dir, 'hit.wav'))
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(path.join(self.dir, 'flappy.TTF') , size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.MAINWINDOW.blit(text_surface, text_rect)        
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
