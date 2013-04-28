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

def mapgen(maptextfile = 'map.txt'):
    #Open the file and read the entire file
    with open(maptextfile, 'r') as f:
        read_data = f.readlines() 
    #get just the map from the read data

    read_data = read_data[2:]
    for index in range(len(read_data)):
        read_data[index] = read_data[index][4:]
        
    is_move_poss = [[0 for c in range(len(read_data[1]))] for r in range(len(read_data))]
    for r in range(len(read_data)):
        for c in range(len(read_data[r])):
            if read_data[r][c] == '#':
                is_move_poss[r][c] = 1
            elif read_data[r][c] == 'O':
                is_move_poss[r][c] = 2
    return is_move_poss

directions = {'up': (0,-1), 'left': (-1,0),'down': (0,1),'right': (1,0)} #a dictionary that converts from direction to a [x,y] vector or tuple

#Defines our generic sprite
class dude(pygame.sprite.Sprite):    
    def __init__(self, position = (200,200), imageloc = 'pacman1.bmp', speed = 5, vhat = (1,0)):
	#Initialize the dood's parameers
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image(imageloc,-1) #sets its image to the called image

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = position #sets the position, in pixels, of the center of the dood
        self.box = pos_to_box(self.rect.center)

        self.vhat = vhat #sets initial direction
        self.speed = speed #sets speed in pixels (?) per cycle (?)

    def update(self):
        #move the dood
        self._move()

class ghost(dude):
    #Dictionary to go from direction to direction unit vector
    def __init__(self, position = (400,400), imageloc = 'ghost1.bmp', speed=5, nextpos = (200,205), target = (500,500), vhat = (1,0), chase= False):
	#Initialize ghost parameters
        dude.__init__(self, position, imageloc, speed)
        self.target = target
        self.chase = chase
        self.nextpos = nextpos
        self.vhat = vhat #sets initial direction
        self.speed = speed #sets speed 

    def get_poss_moves(self):
        possmoves = []
        dir_order = ['up','left','down','right']

        for direct in dir_order:
            temp_vhat = directions[direct]
            temp_new_pos = (self.nextpos[0] + temp_vhat[0]*self.speed, self.nextpos[1]+ temp_vhat[1]*self.speed)
            temp_box_pos = pos_to_box(temp_new_pos)
            ''' if levelmap[temp_box_pos[1]][temp_box_pos[0]]==1:
                possmoves.append(temp_new_pos)'''
            possmoves.append(temp_new_pos)
        return possmoves
            
            
    def new_next_pos(self):
	#Get all possible moves 2 moves in the futre in the order up, left, down, right
        possmoves = self.get_poss_moves()
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
	
    def _move(self):
        if self.rect.center == self.target:
            movingx = 0
            movingy = 0
        else:
            
            movingx =  self.nextpos[0]-self.rect.center[0]
            movingy =  self.nextpos[1]-self.rect.center[1]
        temp_next_move = self.new_next_pos()
        newpos = self.rect.move(movingx,movingy)
        self.rect = newpos
        self.box = pos_to_box(self.rect.center)
	self.nextpos = temp_next_move

    def update_target(self,pacman_pos):
        self.target = pacman_pos

class player(dude):
    def __init__(self, position = (200,200), imageloc = 'pacman1.bmp', speed = 5, vhat = (1,0)):
        dude.__init__(self, position, imageloc, speed, vhat)
        self.original = self.image

    def _turn(self, direct):
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

    def isdead(self, other):
        if self.rect.center == other.rect.center:
            self.kill()
            print "I'm DEAD! I'm ALIVE BUT I'M DEAD!"
        
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

        #move the dude!
        newpos = self.rect.move((movingx,movingy))
        self.rect = newpos
        self.box = pos_to_box(self.rect.center)
        self.isdead(GHOST)
        

class dot(pygame.sprite.Sprite):
    #A dot. They give you points
    def __init__(self, pos = (100,100), imageloc = 'dot.bmp', value = 10):
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image(imageloc,None) #sets its image to the called image
        self.value = value
        self.rect.center = pos
        self.box = pos_to_box(pos)
        self.dead = 0

    def _eaten(self, other):
        if self.box == other.box:
            SCORE.val += self.value
            print(SCORE.val)
            self.kill()

    def update(self):
        self._eaten(pacman)
        

class dotgroup(pygame.sprite.Group):
    #a group of the dots and non-player-non-ghost objects
    def __init__(self, maplist):
        pygame.sprite.Group.__init__(self)
        for i in range(len(maplist)):
            for j in range(len(maplist[i])):
                newpos = box_to_pos((j,i))
                if maplist[i][j] == 1:
                    newdot = dot(newpos)
                    self.add(newdot)
                elif maplist[i][j] == 2:
                    newdot = dot(newpos, 'megadot.bmp', 50)
                    self.add(newdot)

class score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.val = 0
        self.update()
        self.rect = self.image.get_rect().move(100,100)

    def update(self):
        message = "Score: %d" % self.val
        self.image = self.font.render(message, 0, (250,250,250))
        
pygame.init()
screen = pygame.display.set_mode((25*18,29*18))
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

levelmap = mapgen()

pacman = player()
GHOST = ghost()
DOT = dotgroup(levelmap)
SCORE = score()

allsprites = pygame.sprite.RenderPlain(DOT, pacman, GHOST, SCORE)
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
            elif event.key == K_ESCAPE:
                raise SystemExit
    allsprites.update()
    GHOST.update_target(pacman.rect.center)
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()
