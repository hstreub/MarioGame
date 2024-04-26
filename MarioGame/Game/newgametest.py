import pygame
from pygame.locals import *
import sys
import random
import ctypes

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
user32 = ctypes.windll.user32
HEIGHT = 768
WIDTH = 1024
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption("Game")
fullscreen = True
cmddown = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((225,255,0))
        self.rect = self.surf.get_rect()

        self.pos = vec((WIDTH/2, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        
    def move(self):
        self.acc = vec(0,0.5)
 
        pressed_keys = pygame.key.get_pressed()
            
        if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
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
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:
            if hits:
                if hits:
                    if self.pos.y < hits[0].rect.bottom:               
                        self.pos.y = hits[0].rect.top +1
                        self.vel.y = 0
                        self.jumping = False

 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,150), 12))
        self.surf.fill((random.randint(0,255),255,random.randint(0,255)))
        self.rect = self.surf.get_rect(center = (random.randint(10,WIDTH), random.randint(0, HEIGHT)))

    def move(self):
        pass

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False

def plat_gen():
    while len(platforms) < 9:
        width = random.randrange(0,250)
        p  = platform()
        C = True
        while C:
            p = platform()
            p.rect.center = (random.randrange(0,WIDTH),random.randrange(-50,100))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(4, 5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
            if event.key == pygame.K_ESCAPE:
                if fullscreen == True:
                    displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
                    pygame.display.set_caption("GAME")
                    fullscreen = False
                else:
                    displaysurface = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
                    pygame.display.set_caption("GAME")
                    fullscreen == True
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
                
    
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    
    plat_gen()
    displaysurface.fill((0,0,0))
 
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)