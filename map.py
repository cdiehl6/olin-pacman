import pygame
import pygame.draw
from pygame.locals import *

class Map:
    def __init__(self, map, tiles):
        self.tiles=pygame.image.load(tiles)
        l=[line.strip() for line in open(map).readlines()]
        self.map=[[None]*len(l[0])for j in range(len(l))]
        for i in range(len(l[0])):
            for j in range(len(l[0])):
                tile=
    
    def draw(self, view, viewpos):
        sx, sy=view.get_size()
        bx=viewpos[0]/64
        by=viewpos[1]/64
        for x in range(0, sx+64, 64):
