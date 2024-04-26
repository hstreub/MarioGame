import pygame
from pygame.locals import *
import sys
import random
import ctypes
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
user32 = ctypes.windll.user32
HEIGHT = user32.GetSystemMetrics(1)
WIDTH = user32.GetSystemMetrics(0)
displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
# displaysurface = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN) #Fullscreen - my display is 1440 by 900
pygame.display.set_caption("GAME")
cursor_x,cursor_y = 0,0
cmddown = False
fullscreen = True

ACC = 0.5
FRIC = -0.12
FPS = 60
    
FramePerSec = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
            
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_a]:
                self.acc.x = -ACC
        if pressed_keys[K_d]:
                self.acc.x = ACC  

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc      

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -10

    def update(self):
        hits = pygame.sprite.spritecollide(P1 , platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
    
PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)
    
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump() 
            if event.key == pygame.K_ESCAPE:
                    if fullscreen == True:
                        displaysurface = pygame.display.set_mode((WIDTH,HEIGHT)) #exits fullscreen
                        pygame.display.set_caption("MARIO GAME")
                        fullscreen = False
                    else:
                        # displaysurface = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
                        pygame.display.set_caption("MARIO GAME")
                        fullscreen = True


        
        displaysurface.fill((0,0,0))
    P1.update()
    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        P1.move()

    pygame.display.update()
    FramePerSec.tick(FPS)


        

