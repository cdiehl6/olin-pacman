#! /usr/bin/env python

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
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    """Shows lines of text and waits for keyboard input"""
    line1 = loadscreen_text('Welcome to Olin-Pacman!', (100,100))
    line2 = loadscreen_text('Press any key to begin a game', (50,200))
    line3 = loadscreen_text('Press "Escape" to exit', (100,400), 20)
    allsprites = pygame.sprite.RenderPlain(line1, line2, line3)
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise SystemExit
                else: #any key that isn't escape moves the game foreward
                    allsprites.empty()
                    playgame()
                    return
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

def background_gen():
    """make the background image from the map"""
    tile_chars = {'<':(0,0), '-':(1,0), '>':(2,0), '|':(3,0), '#':(3,1), '=': (3,1), '\\': (0,1),'/':(2,1),'O':(3,1)}
    table =  tile_table.load_tile_table('pacmantiles.png',18,18)
    maparray = mapfns.mapchars()
    tiles = [[],[]]
    for row in range(len(maparray)):
        for col in range(len(maparray[0])):
            tile_index = tile_chars[maparray[row][col]]
            background.blit(table[tile_index[0]][tile_index[1]],(col*18,row*18))

def newplayers(yourscore,yourlives):
    """creates players and puts them in allsprites"""
    global pacman
    global BLINKY
    global PINKY
    global INKY
    global CLYDE
    global DOT
    global SCORE
    global HIGHSCORE
    global LIVES
    global MESSAGE
    global GHOSTS
    global allsprites
    pacman = player(lives=yourlives)
    BLINKY = ghosts.Blinky(imageloc = 'blinky.bmp', name = 'blinky',position =  mapfns.box_to_pos((11,14)))
    PINKY = ghosts.Pinky(imageloc = 'pinky.bmp', name = 'pinky',position =  mapfns.box_to_pos((12,14)))
    INKY = ghosts.Inky(imageloc = 'inky.bmp', name = 'inky', position =  mapfns.box_to_pos((13,14)))
    CLYDE = ghosts.Clyde(imageloc = 'clyde.bmp', name = 'clyde', position =  mapfns.box_to_pos((14,14)))
    DOT = dotgroup(levelmap)

    SCORE = score(val = yourscore)
    HIGHSCORE = highscore()
    LIVES = lives()
    MESSAGE = message()

    GHOSTS = pygame.sprite.Group(BLINKY, PINKY, INKY, CLYDE)
    allsprites = pygame.sprite.RenderPlain(pacman, GHOSTS, DOT, SCORE, HIGHSCORE, LIVES, MESSAGE)

def playgame(levelnumber=0, yourscore=0, yourlives=3):
    """Starts a new game at level x"""
    global levelmap
    levelmap = mapfns.mapgen()
    background_gen()
    global chase
    chase = False
    global ghostseaten
    ghostseaten = 0
    global chasetime
    chasetime = 0
    chaseduration = 500
    newplayers(yourscore,yourlives)
    MESSAGE.val = "Level %d" % int(levelnumber+1)
    while 1:
        clock.tick(60)
        if chase:
            if chasetime == 0:
                for i in range(len(GHOSTS.sprites())):
                    GHOSTS.sprites()[i].image, GHOSTS.sprites()[i].rect = dood.load_image('chase.bmp',-1)
                    GHOSTS.sprites()[i].chase = True
            chasetime += 1
            if chasetime == chaseduration:
                chase = False
                for i in range(len(GHOSTS.sprites())):
                    GHOSTS.sprites()[i].chase = False
                BLINKY.image, BLINKY.rect = dood.load_image('blinky.bmp',-1)
                PINKY.image, PINKY.rect = dood.load_image('pinky.bmp',-1)
                INKY.image, INKY.rect = dood.load_image('inky.bmp',-1)
                CLYDE.image, CLYDE.rect = dood.load_image('clyde.bmp',-1)
                ghostseaten = 0
                chasetime = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise SystemExit
                elif event.key == K_SPACE:
                    paused = True
        pygame.key.set_repeat(0,50)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            pacman._turn('left')
        elif keys[K_RIGHT]:
            pacman._turn('right')
        elif keys[K_UP]:
            pacman._turn('up')
        elif keys[K_DOWN]:
            pacman._turn('down')
        allsprites.update()
        BLINKY.update_target(pacman.rect.center,chase)
        PINKY.update_target(pacman.rect.center, pacman.vhat,chase)
        INKY.update_target(pacman.rect.center,pacman.vhat,BLINKY.rect.center,chase)
        CLYDE.update_target(pacman.rect.center,chase)
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
        if len(DOT.sprites()) == 0:
            #if the level ends, start the next one.
            levelnumber += 1
            playgame(levelnumber = levelnumber, yourscore = SCORE.val, yourlives = pacman.lives)

class loadscreen_text(pygame.sprite.Sprite):
    """A sprite that displays text for the loadscreen, centered on the x axis. The x position that is set in the initialization doesn't matter."""
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
    """loads an image from the data folder, and sets its color key."""
    fullname = os.path.join(os.path.dirname(sys.argv[0]),'data', name)
#    try:
    image = pygame.image.load(fullname)

#    except pygame.error, message:
#        print('Cannot load image:')
#        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    """loads the sound files (currently unused, but good for scafolding)"""
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
    """Defines the playable sprite object."""
    def __init__(self, position = mapfns.box_to_pos((5,6)), imageloc = 'pacman.bmp', speed = 3, vhat = (1,0), lives =3):
        dood.dude.__init__(self, position, imageloc, speed, vhat)
        self.original = self.image
        self.lives = lives
        self.startpos = position
    def _turn(self, direct):
        """takes a direction (string), turns the player and makes him go in the way you want him to go"""
        newv=self.directions[direct] #looks up in the directions dictionary
        newpos = (self.rect.center[0] + newv[0]*self.speed, self.rect.center[1] + newv[1]*self.speed)
        if self.vhat == newv: #you can't turn in the direction you're currently going
            return
        try:
            valid_move = self.is_valid_move(levelmap,newpos,1)
            if not valid_move:
                return
        except:
            offscreen = 1
        self.vhat = newv #sets direction
        self.image = self.original #resets the image to left-facing
        center = self.rect.center
        angles = {'up': 90, 'left': 180, 'down': 270, 'right': 0} #dictionary that defines rotation angles
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, angles[direct]) #rotates the image
        self.rect = self.image.get_rect(center=center) #resets the image's center to its original center.

    def isdead(self, other):
        """checks if pacman is dead against another sprite object, or kills the other sprite if it's chasemode"""
        if self.box == other.box:
            global chase
            global chasetime
            if other.chase: #if chasemode is active
                global ghostseaten
                ghostseaten += 1
                SCORE.val += (ghostseaten**2)*100
                other.image, other.rect = dood.load_image(other.name +'.bmp',-1)
                other.reset_to_home()
                other.chase = False
            else:
                self.lives -= 1 #kills the player
                if self.lives: 
                    current_pos = self.rect.center
                    movingx = self.startpos[0] - current_pos[0]
                    movingy = self.startpos[1] - current_pos[1]
                    newpos = self.rect.move((movingx,movingy))
                    self.rect = newpos
                    self.box = mapfns.pos_to_box(self.rect.center)
                    if chase:
                        chase = False
                        chasetime = 0
                        for i in range(len(GHOSTS)):
                            GHOSTS.sprites()[i].chase = False 
                            GHOSTS.sprites()[i].image, GHOSTS.sprites()[i].rect = dood.load_image(GHOSTS.sprites()[i].name + '.bmp',-1)
                   
                    #"I'm DEAD! I'm ALIVE BUT I'M DEAD!"
                    for i in range(len(GHOSTS)):
                        GHOSTS.sprites()[i].reset_to_home()
                else:
                    self.kill()
                    HIGHSCORE.check_highscore(SCORE.val) #checks highscore before ending the game
                    #'Welp, ya done died'
                    game_boot()
    def _move(self):
        """checks if the player can move in the direction it wants, and then moves it if it can, and stops it if it can't."""
        movingx = self.vhat[0]*self.speed #sets how far it will move in the x direction
        movingy = self.vhat[1]*self.speed #sets how far it will move in the y direction
        #the following block lets you float over the edge of the screen
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
                if not self.is_valid_move(levelmap,temp_new_move,1):
                    movingx = 0
                    movingy = 0
            except:
                offscreen = 1
        #move the dude!
        newpos = self.rect.move((movingx,movingy))
        self.rect = newpos
        self.box = mapfns.pos_to_box(self.rect.center)
        for i in range(len(GHOSTS.sprites())):
            self.isdead(GHOSTS.sprites()[i])


class dot(pygame.sprite.Sprite):
    """A point-giving object. Includes special case for power dots, and activates chase mode"""
    def __init__(self, pos = (200,200), imageloc = 'dot.bmp', value = 10):
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image(imageloc,None) #sets its image to the called image
        self.value = value
        self.rect.center = pos
        self.box = mapfns.pos_to_box(pos)
        self.dead = 0
    def _eaten(self, other):
        """destroys dot if it is eaten. Also, activates chasemode"""
        if self.box == other.box:
            SCORE.val += self.value
            if self.value == 50:
                global chase
                global chasetime
                chase = True #engage chase mode
                chasetime = 0
            self.kill()
    def update(self):
        self._eaten(pacman)       

class dotgroup(pygame.sprite.Group):
    """a group of all of the eatable objects"""
    def __init__(self, maplist):
        """generates dots based on the maplist."""
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

#The following classes are all for the bottommost screen. It provides the player with data about the game.
class score(pygame.sprite.Sprite):
    """sprite that displays updating score"""
    def __init__(self, box = (1,30), val=0):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 24)
        self.val = val
        self.update()
        pos = mapfns.box_to_pos(box)
        self.rect = self.image.get_rect().move(pos)
    def update(self):
        self.message = "Score: %d" % self.val
        self.image = self.font.render(self.message, 0, (250,250,250))

class highscore(pygame.sprite.Sprite):
    """Contains all highscore information. The sprite itself displays the highest score."""
    def __init__(self, filename = 'highscore.txt', box = (1,32)):
        """Finds the file where highscores are stored and loads them into local memory. Displays highest score."""
        pygame.sprite.Sprite.__init__(self)
        self.fullname = os.path.join('data', filename)
        try:
            with open(self.fullname, 'r+') as f:
                self.list = pickle.load(f)
        except:
            print('Cannot load highscore file')
            raise(SystemExit)
        self.alltime = self.list[0][0]
        self.font = pygame.font.Font(None,24)
        self.update()
        pos = mapfns.box_to_pos(box)
        self.rect = self.image.get_rect().move(pos)
    def new_highscore(self, score = 0, name = 'Mitch'):
        """Adds a highscore to the highscore list and stores it to the highscore file"""
        newscore = (score, name)
        self.list.append(newscore) #add new score to list
        self.list.sort(reverse = True)  #sort by score
        self.list.pop() #removes lowest score
        self.disp_highscore()
        with open(self.fullname, 'r+') as f:
            pickle.dump(self.list, f)
    def check_highscore(self, score):
        """Checks if you have a high score and asks for your name if you do, then calls new_highscore"""
        for pair in self.list:
            if score > pair[0]:
                background.fill((0,0,0))
                screen.blit(background, (0,0))
                """Shows lines of text and waits for keyboard input"""
                line1 = loadscreen_text('You have a highscore!', (100,100))
                line2 = loadscreen_text(str(score),(100,200))
                line3 = loadscreen_text('Please type your name',(100,400))
                name = ''
                global allsprites
                allsprites = pygame.sprite.RenderPlain(line1,line2,line3)
                while 1:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            raise SystemExit
                        elif event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                raise SystemExit
                            elif event.key == K_BACKSPACE:
                                name = name[:len(name)-1]
                                line3.message = name
                            elif event.key in [K_TAB, K_CLEAR,K_PAUSE,K_EXCLAIM,K_QUOTEDBL,K_LSHIFT,K_RSHIFT,K_LCTRL,K_RCTRL,K_CAPSLOCK,K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                                pass
                            elif event.key == K_SPACE:
                                name += ' '
                                line3.message = name
                            elif event.key == K_RETURN:
                                self.new_highscore(score,name)
                                return
                            else: #any key that isn't escape moves the game foreward
                                name += pygame.key.name(event.key)
                                line3.message = name
                                #game_boot()
                    allsprites.update()
                    screen.blit(background, (0, 0))
                    allsprites.draw(screen)
                    pygame.display.flip()
        self.disp_highscore()
    def disp_highscore(self):
        global allsprites
        allsprites = pygame.sprite.RenderPlain()
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        wait = 0
        GAMEOVER = loadscreen_text('GAME OVER', (100,50))
        allsprites.add(GAMEOVER)
        for i in range(len(self.list)):
            stringy = str(self.list[i][0]) +'  ' +str(self.list[i][1])
            line = loadscreen_text(stringy, (100,150+40*i))
            allsprites.add(line)
        while wait<300:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    raise SystemExit
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        raise SystemExit
                    else:
                        if wait>100:
                            return
            allsprites.update()
            screen.blit(background, (0, 0))
            allsprites.draw(screen)
            pygame.display.flip()
            wait += 1
    def update(self):
        """displays highest score, unless your score beats it, and then it shows your score"""
        if SCORE.val >= self.alltime:
            self.alltime = SCORE.val
        self.message = "Highscore: %d" % self.alltime
        self.image = self.font.render(self.message, 0, (250,250,250))

class lives(pygame.sprite.Sprite):
    """shows the number of lives the player has"""
    def __init__(self, box = (10,30)):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 24)
        self.update()
        pos = mapfns.box_to_pos(box)
        self.rect = self.image.get_rect().move(pos)
    def update(self):
        self.message = "Lives: %d" % pacman.lives
        self.image = self.font.render(self.message, 0, (250,250,250))

class message(pygame.sprite.Sprite):
    """Displays a message of your choosing."""
    def __init__(self, box = (10,32), val='Olin-Pacman!'):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.val = val
        self.update()
        pos = mapfns.box_to_pos(box)
        self.rect = self.image.get_rect().move(pos)
    def update(self):
        """displays self.val"""
        self.message = self.val
        self.image = self.font.render(self.message, 0, (250,250,250))


#Begin the game environment!

pygame.init()
screen = pygame.display.set_mode((24*18,(29+5)*18),pygame.FULLSCREEN)
pygame.display.set_caption('Olin-Man')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))
screen.blit(background, (0,0))
pygame.display.flip()

clock = pygame.time.Clock()
game_boot()
pygame.display.flip()
