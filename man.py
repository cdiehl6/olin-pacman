import os, sys
import pygame
from pygame.locals import *
from math import sqrt, floor
import pickle
import dood
import ghosts
import mapfns
import pygame.draw
import tile_table



if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sounds disabled'

def game_boot():
    line1 = loadscreen_text('Welcome to Olin-Pacman!', (100,100))
    line2 = loadscreen_text('Press any key to begin a game', (50,200))
    line3 = loadscreen_text('Press "Escape" to exit', (100,400), 20)
    allsprites = pygame.sprite.RenderPlain(line1, line2, line3)
    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise SystemExit
                else:
                    allsprites.empty()
                    return
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

class loadscreen_text(pygame.sprite.Sprite):
    def __init__(self, message = 'text', pos= (100,250), fontsize = 36):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, fontsize)
        self.message = message
        self.update()
        self.rect = self.image.get_rect().move(pos)
        self.rect.centerx = background.get_width()/2

    def update(self):
        self.image = self.font.render(self.message, 0, (250,250,250))


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
        print('Cannot load sound:', name)
        raise(SystemExit, message)
    return sound



class player(dood.dude):
    def __init__(self, position = (100,100), imageloc = 'pacman.bmp', speed = 4, vhat = (1,0), lives =3):
        dood.dude.__init__(self, position, imageloc, speed, vhat)
        self.original = self.image
        self.lives = lives
        self.startpos = position

    def _turn(self, direct):
        #takes a string as an input of 'up' 'down' 'left' or 'right' and turns pacman and makes him go in the way you want him to go
        newv=self.directions[direct] #looks up in the directions dictionary

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
        if self.box == other.box:
            global chase
            global chasetime
            if other.chase:
                global ghostseaten
                ghostseaten += 1
                SCORE.val += (ghostseaten**2)*100
                other.reset_to_home()
                other.image, other.rect = dood.load_image(other.name+'.bmp',-1)
                other.chase = False
            else:
                self.lives -= 1
                if self.lives:
                    current_pos = self.rect.center
                    movingx = self.startpos[0] - current_pos[0]
                    movingy = self.startpos[1] - current_pos[1]
                    newpos = self.rect.move((movingx,movingy))
                    self.rect = newpos
                    self.box = mapfns.pos_to_box(self.rect.center)
                    BLINKY.reset_to_home()
                    PINKY.reset_to_home()
                    INKY.reset_to_home()
                    CLYDE.reset_to_home()
                    if chase:
                        chase = False
                        BLINKY.chase = False
                        PINKY.chase = False
                        INKY.chase = False
                        CLYDE.chase = False
                        BLINKY.image, BLINKY.rect = dood.load_image('blinky.bmp',-1)
                        PINKY.image, PINKY.rect = dood.load_image('pinky.bmp',-1)
                        INKY.image, INKY.rect = dood.load_image('inky.bmp',-1)
                        CLYDE.image, CLYDE.rect = dood.load_image('clyde.bmp',-1)
                        chasetime = 0
                    
                    
                    print("I'm DEAD! I'm ALIVE BUT I'M DEAD!")
                else:
                    self.kill()
                    print('Welp, ya done died')
        
    def _move(self):

        movingx = self.vhat[0]*self.speed #sets how far it will move in the x direction
        movingy = self.vhat[1]*self.speed #sets how far it will move in the y direction

        #the following if/elif block makes the dood stop if it hits the side of the window.
        if self.rect.left <= self.area.left and self.vhat==self.directions['left']: #left edge
            movingx = self.area.right - self.area.left
        elif self.rect.right >= self.area.right and self.vhat == self.directions['right']: #right edge
            movingx = self.area.left - self.area.right
        elif self.rect.top <= self.area.top and self.vhat==self.directions['up']: #top edge
            movingy = self.area.bottom - self.area.top
        elif self.rect.bottom >= self.area.bottom and self.vhat == self.directions['down']: #bottom edge
            movingy = self.area.top - self.area.bottom
        else:
            try:
                centerpos = self.rect.center
                temp_new_move = (centerpos[0] + movingx, centerpos[1] + movingy)
                temp_new_box = mapfns.pos_to_box(temp_new_move)
                if levelmap[temp_new_box[1]][temp_new_box[0]] == 0:
                    movingx = 0
                    movingy = 0
            except:
                print('off screen')

        #move the dude!
        newpos = self.rect.move((movingx,movingy))
        self.rect = newpos
        self.box = mapfns.pos_to_box(self.rect.center)
        self.isdead(BLINKY)
        self.isdead(INKY)
        self.isdead(PINKY)
        self.isdead(CLYDE)

class dot(pygame.sprite.Sprite):
    #A dot. They give you points
    def __init__(self, pos = (200,200), imageloc = 'dot.bmp', value = 10):
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image(imageloc,None) #sets its image to the called image
        self.value = value
        self.rect.center = pos
        self.box = mapfns.pos_to_box(pos)
        self.dead = 0

    def _eaten(self, other):
        if self.box == other.box:
            SCORE.val += self.value
            if self.value == 50:
                print('chase engaged')
                global chase
                chase = True
            self.kill()


    def update(self):
        self._eaten(pacman)        

class dotgroup(pygame.sprite.Group):
    #a group of the dots and non-player-non-ghost objects
    def __init__(self, maplist):
        pygame.sprite.Group.__init__(self)
        for i in range(len(maplist)):
            for j in range(len(maplist[i])):
                newpos = mapfns.box_to_pos((j+1,i+1))
                if maplist[i][j] == 1:
                    newdot = dot(newpos)
                    self.add(newdot)
                elif maplist[i][j] == 2:
                    newdot = dot(newpos, 'megadot.bmp', 50)
                    self.add(newdot)

class score(pygame.sprite.Sprite):
    def __init__(self, pos= (300,300)):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.val = 0
        self.update()
        self.rect = self.image.get_rect().move(pos)

    def update(self):
        self.message = "Score: %d" % self.val
        self.image = self.font.render(self.message, 0, (250,250,250))

class highscore(pygame.sprite.Sprite):
    def __init__(self, filename = 'highscore.txt', pos = (300,350)):
        pygame.sprite.Sprite.__init__(self)
        self.fullname = os.path.join('data', filename)
        try:
            with open(self.fullname, 'r+') as f:
                self.list = pickle.load(f)
        except:
            print('Cannot load highscore file')
            raise(SystemExit)
        self.alltime = self.list[0][0]

        self.font = pygame.font.Font(None,20)
        self.update()
        self.rect = self.image.get_rect().move(pos)
       
    def new_highscore(self, score = 0, name = 'Mitch'):
        newscore = (score, name)
        self.list.append(newscore) #add new score to list
        self.list.sort(reverse = True)  #sort by score
        self.list.pop() #removes lowest score
        print self.list
        with open(self.fullname, 'r+') as f:
            pickle.dump(self.list, f)

    def check_highscore(self, score):
        for pair in self.list:
            if score > pair[0]:
                name = raw_input('You got a high score, what is your name? ')
                new_highscore(score,name)
                return
        return

    def update(self):
        if SCORE.val >= self.alltime:
            self.alltime = SCORE.val
        
        self.message = "Highscore: %d" % self.alltime
        self.image = self.font.render(self.message, 0, (250,250,250))

pygame.init()
levelmap = mapfns.mapgen()
screen = pygame.display.set_mode((24*18,29*18))
pygame.display.set_caption('PacMan')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())

background = background.convert()
background.fill((0,0,0))

screen.blit(background, (0,0))
pygame.display.flip()

game_boot()



tile_chars = {'<':(0,0), '-':(1,0), '>':(2,0), '|':(3,0), '#':(3,1), '=': (3,1), '\\': (0,1),'/':(2,1),'O':(3,1)}
table =  tile_table.load_tile_table('pacmantiles.png',18,18)
maparray = mapfns.mapchars()
tiles = [[],[]]
'''for x, row in enumerate(table):
    for y, tile in enumerate(row):
        screen.blit(tile, (x*18, y*18))'''
for row in range(len(maparray)):
    for col in range(len(maparray[0])):
        tile_index = tile_chars[maparray[row][col]]
        background.blit(table[tile_index[0]][tile_index[1]],(col*18,row*18))

pygame.display.flip()



pacman = player()
BLINKY = ghosts.Blinky(imageloc = 'blinky.bmp', name = 'blinky')
PINKY = ghosts.Pinky(imageloc = 'pinky.bmp', name = 'pinky')
INKY = ghosts.Inky(imageloc = 'inky.bmp', name = 'inky')
CLYDE = ghosts.Clyde(imageloc = 'clyde.bmp', name = 'clyde')
DOT = dotgroup(levelmap)
SCORE = score()
HIGHSCORE = highscore()


chase  = False
chasetime = 0
ghostseaten = 0


allsprites = pygame.sprite.RenderPlain(DOT, pacman, BLINKY, PINKY, INKY, CLYDE, SCORE, HIGHSCORE)
clock = pygame.time.Clock()

def playgame(levelnumber=0):
    global chase
    global ghostseaten
    global chasetime
    chaseduration = 1000
    while 1:
        clock.tick(60)
        if chase:
            if chasetime == 0:
                BLINKY.image, BLINKY.rect = dood.load_image('chase.bmp',-1)
                PINKY.image, PINKY.rect = dood.load_image('chase.bmp',-1)
                INKY.image, INKY.rect = dood.load_image('chase.bmp',-1)
                CLYDE.image, CLYDE.rect = dood.load_image('chase.bmp',-1)
                BLINKY.chase = True
                PINKY.chase = True
                INKY.chase = True
                CLYDE.chase = True
            chasetime += 1
            if chasetime == chaseduration:
                chase = False
                BLINKY.image, BLINKY.rect = dood.load_image('blinky.bmp',-1)
                PINKY.image, PINKY.rect = dood.load_image('pinky.bmp',-1)
                INKY.image, INKY.rect = dood.load_image('inky.bmp',-1)
                CLYDE.image, CLYDE.rect = dood.load_image('clyde.bmp',-1)
                BLINKY.chase = False
                PINKY.chase = False
                INKY.chase = False
                CLYDE.chase = False
                ghostseaten = 0
                chasetime = 0
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
                elif event.key == K_SPACE:
                    paused = True
        allsprites.update()
        BLINKY.update_target(pacman.rect.center,chase)
        PINKY.update_target(pacman.rect.center, pacman.vhat,chase)
        INKY.update_target(pacman.rect.center,pacman.vhat,BLINKY.rect.center,chase)
        CLYDE.update_target(pacman.rect.center,chase)
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
playgame()
