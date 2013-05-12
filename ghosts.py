import os, sys
import pygame
from pygame.locals import *
from math import sqrt, floor
import pickle
import dood
import mapfns

class ghost(dood.dude):
    home_boxes = ((11,12),(12,12),(12,11),(12,12),(12,13),(12,14))
    def __init__(self, position = mapfns.box_to_pos((14,14)), imageloc = 'ghost1.bmp', speed=2, target = (0,0), vhat = (0,1), chase= False, name = 'Paul'):
	#Initialize ghost parameters
        dood.dude.__init__(self, position, imageloc, speed)
        self.target = target
        self.vhat = vhat #sets initial direction
        self.speed = speed #sets speed
        self.startpos = position
        self.nextpos = (self.rect.center[0] + self.vhat[0]*self.speed, self.rect.center[1] + self.vhat[1]*self.speed)
        self.chase = chase
        self.name = name
    def get_poss_moves(self):
        #New next possible moves for the ghost
        possmoves = []
        dir_order = ['up','left','down','right']
        validmove = True
        sideoffsets = ((0,-8),(-8,0),(0,8),(8,0))
        tunnel_boxes = ((13,0),(13,1),(13,2),(13,3),(13,4),(13,19),(13,20),(13,21),(13,22),(13,23))
        current_box_val = 1
        for side in sideoffsets:
            sidepos = (self.rect.center[0] + side[0], self.rect.center[1] + side[1])
            sidebox = mapfns.pos_to_box(sidepos)
            if levelmap[sidebox[1]][sidebox[0]] == 0.5:
                current_box_val = 0.5
        for direct in dir_order:
            temp_vhat = self.directions[direct]
            temp_new_pos = (self.nextpos[0] + temp_vhat[0]*self.speed, self.nextpos[1]+ temp_vhat[1]*self.speed)
            if current_box_val == 0.5:
                validmove = self.is_valid_move(levelmap,temp_new_pos,0.5,tunnel_boxes)
            else:
                validmove = self.is_valid_move(levelmap,temp_new_pos,1,tunnel_boxes)
            if temp_new_pos == self.rect.center:
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
    def reset_to_home(self):
        movingx =  self.startpos[0]-self.rect.center[0]
        movingy =  self.startpos[1]-self.rect.center[1]
        newpos = self.rect.move((movingx,movingy))
        self.rect = newpos
        self.box = mapfns.pos_to_box(self.rect.center)
        self.vhat = (0,1)
        self.nextpos = (self.rect.center[0] + self.vhat[0]*self.speed, self.rect.center[1] + self.vhat[1]*self.speed)
        
class Blinky(ghost):
	#Blinky's target is pacman
    def update_target(self,pac_pos,chase):
        if levelmap[self.box[1]][self.box[0]] == 0.5:
            self.target = (11,11)
        elif self.chase:
            self.target = (self.area.left,self.area.top)
        else:
            self.target = pac_pos
class Pinky(ghost):
	#Pinky's target is 4 tiles offset in the direction pacman is moving, except when pacman is moving up. Then it is 4 tiles up and 4 to the left.
    def update_target(self,pac_pos,pac_vhat,chase):
        if levelmap[self.box[1]][self.box[0]] == 0.5:
            self.target = (11,11)
        elif self.chase:
            self.target = (self.area.right,self.area.top)
        else:
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
    def update_target(self,pac_pos,pac_vhat,blinky_pos,chase):
        if levelmap[self.box[1]][self.box[0]] == 0.5:
            self.target = (11,11)
        elif self.chase:
            self.target = (self.area.right,self.area.bottom)
        else:
            if pac_vhat == self.directions['left']:
                self.target = [pac_pos[0] - 4*18, pac_pos[1]]
            elif pac_vhat == self.directions['right']:
                self.target = [pac_pos[0] + 4*18, pac_pos[0]]
            elif pac_vhat == self.directions['down']:
                self.target = [pac_pos[0], pac_pos[1] + 4*18]
            elif pac_vhat == self.directions['up']:
                self.target = [pac_pos[0]-4*18, pac_pos[1] - 4*18] 

class Clyde(ghost):
    #Clyde targets pacman when pacman is more than 8 squares away, and the bottom left corner when pacman is closer
    def update_target(self,pac_pos,chase):
        if levelmap[self.box[1]][self.box[0]] == 0.5:
            self.target = (11,11)
        elif self.chase:
            self.target = (self.area.left,self.area.bottom)
        else:
            #get the distance from Clyde to pacman
            dist = sqrt((self.rect.center[0]-pac_pos[0])**2 + (self.rect.center[1]-pac_pos[1])**2)
            #set the target
            if dist >= 8*18:
                self.target = pac_pos
            else:
                self.target = [0,29*18]
            #This should be the bottom left corner of the maze (I don't know what that is yet]

levelmap = mapfns.mapgen()
