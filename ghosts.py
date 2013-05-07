import os, sys
import pygame
from pygame.locals import *
from math import sqrt, floor
import pickle
import dood
import mapfns

class ghost(dood.dude):
    #Dictionary to go from direction to direction unit vector
    def __init__(self, position = mapfns.box_to_pos((2,5)), imageloc = 'ghost1.bmp', speed=2, target = (0,0), vhat = (0,1), chase= False):
	#Initialize ghost parameters
        dood.dude.__init__(self, position, imageloc, speed)
        self.target = target
        self.chase = chase
        self.vhat = vhat #sets initial direction
        self.speed = speed #sets speed

        self.nextpos = (self.rect.center[0] + self.vhat[0]*self.speed, self.rect.center[1] + self.vhat[1]*self.speed)
        
    def get_poss_moves(self):
        possmoves = []
        dir_order = ['up','left','down','right']
        validmove = True
        sideoffsets = ((0,-9),(-9,0),(0,7),(7,0))
        tunnel_boxes = ((13,0),(13,1),(13,2),(13,3),(13,4),(13,19),(13,20),(13,21),(13,22),(13,23))
        for direct in dir_order:
            temp_vhat = self.directions[direct]
            temp_new_pos = (self.nextpos[0] + temp_vhat[0]*self.speed, self.nextpos[1]+ temp_vhat[1]*self.speed)
            temp_box_pos = mapfns.pos_to_box(temp_new_pos)
            if temp_new_pos == self.rect.center:
                validmove = False
            if not(temp_new_pos[0]% 18 ==  9 or temp_new_pos[1] % 18 == 9):
                validmove =False
            if not(levelmap[temp_box_pos[1]][temp_box_pos[0]]):
                validmove = False
            for sideoff in sideoffsets:
                side_pos = (temp_new_pos[0]+sideoff[0],temp_new_pos[1]+sideoff[1])
                side_box = mapfns.pos_to_box(side_pos)
                if levelmap[side_box[1]][side_box[0]] == 0:
                    validmove = False
                for ill_box in tunnel_boxes:
                    if (side_box[1],side_box[0]) == ill_box:
                        validmove = False
                
            if validmove:
                possmoves.append(temp_new_pos)
            validmove = True
        return possmoves 
        
    def new_next_pos(self):
        d = 0
	#Get all possible moves 2 moves in the futre in the order up, left, down, right
        possmoves = self.get_poss_moves()
        if possmoves == []:
            return self.rect.center
	#Find the distance from each possible move to the target tile
        possdist = []
        for move in possmoves:
            possdist.append(sqrt((self.target[0] - move[0])**2 + (self.target[1] - move[1])**2))
	#Find the move that is closest (if two are the same, the order is: up, left, down right)

        leastdistindex = possdist.index(min(possdist))
        return possmoves[leastdistindex]

    def _move(self):
        temp_next_move = self.new_next_pos()
        movingx =  self.nextpos[0]-self.rect.center[0]
        movingy =  self.nextpos[1]-self.rect.center[1]
        vhat = (movingx/self.speed, movingy/self.speed)
        newpos = self.rect.move((movingx,movingy))
 
        self.rect = newpos
        self.box = mapfns.pos_to_box(self.rect.center)
	self.nextpos = temp_next_move
        self.vhat = vhat

    def update_target(self,pac_pos):
        self.target = (0,0)

class Blinky(ghost):
	#Blinky's target is pacman
    def update_target(self,pac_pos):
        self.target = pac_pos
class Pinky(ghost):
	#Pinky's target is 4 tiles offset in the direction pacman is moving, except when pacman is moving up. Then it is 4 tiles up and 4 to the left.

#Right now, just adding tiles, not pixels BTW
    def update_target(self,pac_pos,pac_vhat):
        if pac_vhat == self.directions['left']:
            self.target = [pac_pos[0] - 4*18, pac_pos[1]]
        elif pac_vhat == self.directions['right']:
            self.target = [pac_pos[0] + 4*18, pac_pos[0]]
        elif pac_vhat == self.directions['down']:
            self.target = [pac_pos[0], pac_pos[1] + 4*18]
        elif pac_vhat == self.directions['up']:
            self.target = [pac_pos[0]-4*18, pac_pos[1] - 4*18] 

class Inky(ghost):
#I don't even know how to describe this target tile. The dossier says this: "To determine Inky's target, we must first establish an intermediate offset two tiles in front of Pac-Man in the direction he is moving (represented by the tile bracketed in green above). Now imagine drawing a vector from the center of the red ghost's current tile to the center of the offset tile, then double the vector length by extending it out just as far again beyond the offset tile.
    def update_target(self,pac_pos,pac_vhat,blinky_pos):
        offsettile = [0,0]
        if pac_vhat == self.directions['left']:
            offsettile = [pac_pos[0] - 2*18, pac_pos[1]]
        elif pac_vhat == self.directions['right']:
            offsettile = [pac_pos[0] + 2, pac_pos[0]]
        elif pac_vhat == self.directions['down']:
            offsettile = [pac_pos[0], pac_pos[1] - 2*18]
        elif pac_vhat == self.directions['up']:
            offsettile = [pac_pos[0]-2*18, pac_pos[1] + 2*18]
        self.target = [2*offsettile[0] - blinky_pos[0], 2*offsettile[1] - blinky_pos[1]]

class Clyde(ghost):
    #Clyde targets pacman when pacman is more than 8 squares away, and the bottom left corner when pacman is closer
    def update_target(self,pac_pos):
        #get the distance from Clyde to pacman
        dist = sqrt((self.rect.center[0]-pac_pos[0])**2 + (self.rect.center[1]-pac_pos[1])**2)
        #set the target
        if dist >= 8*18:
            self.target = pac_pos
        else:
            self.target = [0,29*18]
            #This should be the bottom left corner of the maze (I don't know what that is yet]

levelmap = mapfns.mapgen()
