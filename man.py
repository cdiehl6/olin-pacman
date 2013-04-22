import os, sys
import pygame
from pygame.locals import *

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sounds disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print('Cannot load image:', name)
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print('Cannot load sound:', wav)
        raise(SystemExit, message)
    return sound

from math import sqrt
#get the key in the dictionary from the value
def reverse_lookup(d, v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError

#Defines the generic playable character object
class dude(pygame.sprite.Sprite):
    #Dictionary to go from direction to direction unit vector
    directions = {'up': [0,1], 'left': [-1,0],'down': [0,-1],'right':[1,0]}
    
    def __init__(self):
	#Initialize ghost parameters
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image('pacman.bmp',-1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10

        self.vhat = [0,-1]
        self.speed = 10

    def turn(self,direct):
        newv=self.directions[direct]
        if self.vhat == newv:
            return
        print(direct)
        self.vhat = newv
        self.image = self.original
        center = self.rect.center
        angles = {'up': 90, 'left': 180, 'down': 270, 'right': 0}
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, angles[direct])
        self.rect = self.image.get_rect(center=center)
        
    def update(self):
        #move the dood
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('pacman')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))

if pygame.font:
    font = pygame.font.Font(None,36)
    text = font.render("PACMAN!", 1, (255,255,255))
    textpos=text.get_rect(centerx=background.get_width()/2)
    background.blit(text, textpos)

screen.blit(background, (0,0))
pygame.display.flip()

pacman = dude()

allsprites = pygame.sprite.RenderPlain(pacman)
clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                pacman.turn('left')
            elif event.key == K_RIGHT:
                pacman.turn('right')
            elif event.key == K_UP:
                pacman.turn('up')
            elif event.key == K_DOWN:
                pacman.turn('down')
    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()
