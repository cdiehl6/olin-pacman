import os
import sys
import pygame
from pygame.locals import *
import mapfns

#Load the image for each sprite
def load_image(name, colorkey=None):
    #Each image will be stored in the data folder. This appends that to the file path
    fullname = os.path.join('data', name)
    try:
        #Load the image
        image = pygame.image.load(fullname)
    #If there's an error, display that the image cannot be loaded and quit the game
    except pygame.error, message:
        print('Cannot load image:', name)
        raise SystemExit, message
    #Create a copy that draws more quickly to the screen
    image = image.convert()
    #Get the color key for that image
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    #return the image and the corresponding rectangle
    return image, image.get_rect()

#Get the dictionary entry given the key
def reverse_lookup(d, v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError

#Defines our generic sprite
class dude(pygame.sprite.Sprite):
    #A dictionary for converting from direction to a velocity unit vector.
    directions = {'up': (0,-1), 'left': (-1,0),'down': (0,1),'right': (1,0)} 
    def __init__(self, position = (100,100), imageloc = 'pacman1.bmp', speed = 8, vhat = (0,-1)):
	#Initialize the dood's parameers
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image(imageloc,-1) #sets its image to the called image

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = position #sets the position, in pixels, of the center of the dood
        self.box = mapfns.pos_to_box(self.rect.center)

        self.vhat = vhat #sets initial direction
        self.speed = speed #sets speed in pixels (?) per cycle (?)

    def is_valid_move(self,levelmap,poss_move,lowestvalid,invalid_boxes = (-1,-1)):
        side_offsets = ((0,8),(8,0),(0,-8),(-8,0))
        poss_box = mapfns.pos_to_box(poss_move)
        if levelmap[poss_box[1]][poss_box[0]] == 0:
            return False
        elif not(poss_move[0] % 18 == 9 or poss_move[1] % 18 == 9):
            return False
        for side in side_offsets:
            side_pos = (poss_move[0] + side[0], poss_move[1] + side[1])
            side_box = mapfns.pos_to_box(side_pos)
            if levelmap[side_box[1]][side_box[0]] < lowestvalid:
                return False
            for space in invalid_boxes:
                if (side_box[1],side_box[0]) == space:
                    return False
    
        return True
    def update(self):
        #move the dood
        self._move()
