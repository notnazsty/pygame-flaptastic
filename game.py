import pygame
import time
import os
import random

# Initialize pygame
pygame.init()
pygame.font.init()
#Create win
win = pygame.display.set_mode((500, 640))

#Title and Icon
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('flappy.png')
pygame.display.set_icon(icon)

#Clock
clock = pygame.time.Clock()
score = 0
endState = False

#Sprites
bgb4 = pygame.image.load('bckgrnd.png')
bg = pygame.transform.scale(bgb4, (500,640))
tpil = pygame.image.load('toppil.png')
floor = pygame.image.load('floor.png')
S_FONT = pygame.font.SysFont("comicsans", 50)

#Player Class
class player(object):
    global endState
    sprites = [pygame.image.load('bird0.png'), pygame.image.load('bird1.png')]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.birdstage = 0
        self.jump = False
        self.vel = 0
        self.playerImg = pygame.image.load('bird0.png')
        self.tick_elapsed = 0
        self.score = 0
    def redrawPlayer(self):
        if self.birdstage != 27:
            self.playerImg = player.sprites[self.birdstage//3 % 2]
        else:
            self.birdstage = 0
        if bird.vel <= -3:
            self.playerImg = pygame.transform.rotate(self.playerImg, -30)
        elif bird.vel >= 3:
            self.playerImg = pygame.transform.rotate(self.playerImg, 30)
        win.blit(self.playerImg, (self.x, self.y))
    def move(self):
        global endState
        if keys[pygame.K_SPACE] and self.y > 0 and self.vel < 8 and not endState:
            self.vel = 6
            self.jump = 0
        else:
            self.vel -= 0.75
        if self.y - self.vel < 550 and self.y - self.vel > 0:
            self.y -= bird.vel
        elif self.y - self.vel >= 550:
            self.y = 550
            time.sleep(0.5)
            endState = True
        elif self.y - self.vel <= 0:
            self.y = 0
        self.birdstage += 1
        self.tick_elapsed = 0
    def mask_bird(self):
        return pygame.mask.from_surface(self.playerImg)

class pillar():
    number_pillar = 0
    def __init__(self, x, boty, gap):
        self.x = x
        self.boty = boty
        self.height = 637
        self.gap = gap
        self.topy = self.boty - self.gap - self.height
        self.sprite = pygame.image.load('toppil.png')
        self.passed = False
        self.vel = 2
        pillar.number_pillar += 1
        self.botpil = pygame.transform.rotate(self.sprite, 180)   
    def redrawPil(self):
        win.blit(self.botpil, (self.x, self.boty))
        win.blit(self.sprite, (self.x, self.topy))
    def movePillar(self):
        self.x -= self.vel
    def collide(self, bird):
        bird_mask = bird.mask_bird()
        top_mask = pygame.mask.from_surface(self.sprite)
        bot_mask = pygame.mask.from_surface(self.botpil)
        
        top_offset = (self.x - bird.x, self.topy - round(bird.y))
        bot_offset = (self.x - bird.x, self.boty - round(bird.y))
        
        b_point = bird_mask.overlap(bot_mask, bot_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        else:
            return False
class Base:
    """
    REDO
    """
    VEL = 2
    WIDTH = floor.get_width()
    IMG = floor
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
def pillarGen():
    tempy = random.randrange(200, 500)
    poles.append(pillar(640+tpil.get_width(), tempy, 120))

poles = []
#All Players
bird = player(235, 305, 30, 43)
plyr = [bird]
base = Base(560)
def reDraw():
    win.blit(bg, (0,0))
    for i in poles:
        i.redrawPil()
    base.draw(win)
    for i in plyr:
        i.redrawPlayer()
    text = S_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (250 - (text.get_width() / 2), 10))
    if endState:
        win.fill((0, 0 ,0))
        endText = S_FONT.render("Score: " + str(score), 1, (0,255,0))
        win.blit(endText, (250 - (endText.get_width() / 2), 320 - (endText.get_height() / 2)))
    pygame.display.update()

def moves():
    global score
    global running
    global endState
    base.move()
    removePil = [ ]
    active_poles = poles
    if len(removePil) != 0:
        active_poles = poles.remove(removePil)
    if poles == []:
        pillarGen()
    for i in plyr:
        i.move() 
    if not endState:
        for pole in active_poles:
            if not pole.passed and pole.x + pole.sprite.get_width() <= bird.x:
                pole.passed = True
                bird.score += 1
                score += 1
            if pole.x + pole.sprite.get_width() < 0:
                pole
                removePil.append(active_poles)
            else:
                pole.movePillar()
            if pole.x == 480:
                pillarGen()
            if pole.collide(bird):
                time.sleep(0.5)
                endState = True
#Game Loop
running = True
while running:
    global End
    clock.tick(27)
    win.fill((135, 206, 235))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    moves()
    reDraw()

print("Score: ", score)
pygame.quit()
