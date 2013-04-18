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
    image = image.convert
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
        print 'Cannot load sound:', wav)
        raise SystemExit, message
    return sound

from math import sqrt
#get the key in the dictionary from the value
def reverse_lookup(d, v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError

#Defines the generic playable character object
class dude(object):
    #Dictionary to go from direction to direction unit vector
    directions = {'up': [0,1], 'left': [0,-1],'down': [0,-1],'right':[1,0]}
    def __init__(self, name = 'Pacman', position = [0,0], nextpos = [0,1], vhat = [-1,0], speed = 10):
	#Initialize ghost parameters
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image('pacman.bmp',-1)
        self.position = position
        self.nextpos = nextpos
        self.vhat = vhat
        self.speed = speed
    def update(self):
        #move the dood
        self.shipRect.center = (


py.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('pacman')
pygame.mouse.set_visible(0)

background = pygame.Surface(sceen.get_size())
background = background.convert()
background.fill = ((0,0,0))
    
