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

from math import sqrt, floor
#get the key in the dictionary from the value
def reverse_lookup(d, v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError

def pos_to_box(position = (0,0), boxsize=18):
    boxx = int(floor(position[0]/boxsize))
    boxy = int(floor(position[1]/boxsize))
    return (boxx, boxy)

def box_to_pos(box = (0,0), boxsize=18):
    posx = int(box[0]*boxsize - floor(boxsize/2))
    posy = int(box[1]*boxsize - floor(boxsize/2))
    return (posx, posy)

directions = {'up': [0,-1], 'left': [-1,0],'down': [0,1],'right':[1,0]} #a dictionary that converts from direction to a [x,y] vector or tuple

#Defines the generic playable character object. 
class dude(pygame.sprite.Sprite):    
    def __init__(self, position = (200,200), imageloc = 'pacman.bmp'):
	#Initialize the dood's parameters
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image(imageloc,-1) #sets its image to the called image
        self.original = self.image #sets an unchanging image as its default orientation (facing left) (yes, that's important for how the function turns things later)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = position #sets the position, in pixels, of the center of the dood

        self.vhat = [1,0] #sets initial direction
        self.speed = 5 #sets speed in pixels (?) per cycle (?)

    def _turn(self,direct):
        #takes a string as an input of 'up' 'down' 'left' or 'right' and turns pacman and makes him go in the way you want him to go
        newv=directions[direct] #looks up in the directions dictionary
        if self.vhat == newv: #does nothing when you try to turn in the direction that you're already turning.
            return
        
        self.vhat = newv #sets direction to the direction you are trying to go
        self.image = self.original #resets the image to its original (left-facing) orientation
        center = self.rect.center
        angles = {'up': 90, 'left': 180, 'down': 270, 'right': 0} #dictionary that defines rotation angles
        
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, angles[direct]) #rotates the image from its original position
        self.rect = self.image.get_rect(center=center) #resets the image's center to its original center.
        
    def _move(self):
        movingx = self.vhat[0]*self.speed #sets how far it will move in the x direction
        movingy = self.vhat[1]*self.speed #sets how far it will move in the y direction

        #the following if/elif block makes the dood stop if it hits the side of the window.
        if self.rect.left<self.area.left and self.vhat==directions['left']: #left edge
            movingx = 0
        elif self.rect.right>self.area.right and self.vhat == directions['right']: #right edge
            movingx = 0
        elif self.rect.top < self.area.top and self.vhat==directions['up']: #top edge
            movingy = 0
        elif self.rect.bottom > self.area.bottom and self.vhat == directions['down']: #bottom edge
            movingy = 0

        #the next two lines move the dood
        newpos = self.rect.move((movingx,movingy))
        self.rect = newpos
            
    def update(self):
        #move the dood
        self._move()

class ghost(dude):
    #Dictionary to go from direction to direction unit vector
    def __init__(self, position = (20,20), imageloc = 'ghost.bmp', nextpos = [0,1], target = [-1,-1], vhat = [0,1], chase= False, speed =10):
	#Initialize ghost parameters
        dude.__init__(self, position, imageloc)
        self.target = target
        self.chase = chase
        self.nextpos = nextpos

    def new_next_pos(self):
	#Get all possible moves 2 moves in the futre in the order up, left, down, right
        possmoves = [[0,2],[-1,1],[0,0],[1,1]] 
	#Remve the current position (the ghost cannot reverse direction)
        possmoves.remove(self.position)
	#Find the distance from each possible move to the target tile
        possdist = []
        for move in possmoves:
            possdist.append(sqrt((self.target[0] - move[0])**2 + (self.target[1] - move[1])**2))
	#Find the move that is closest (if two are the same, the order is: up, left, down right)
        leastdistindex = 0
        for d in range(len(possdist)):
            if possdist[d] < possdist[leastdistindex]:
                leastdistindex = d 
	#Return the new next position
        return possmoves[leastdistindex]
	
    def make_move(self):
	#Get the new next move
        temp_next_move = self.new_next_pos
	#Make the current positon the old next position
        self.position = self.nextpos
	#make the next position, the new next move
        self.nextpos = temp_next_move


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
GHOST = ghost()

allsprites = pygame.sprite.RenderPlain(pacman, GHOST)
clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            raise SystemExit
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                pacman._turn('left')
            elif event.key == K_RIGHT:
                pacman._turn('right')
            elif event.key == K_UP:
                pacman._turn('up')
            elif event.key == K_DOWN:
                pacman._turn('down')
    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()
