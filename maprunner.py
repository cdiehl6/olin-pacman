import pygame
import pygame.draw
from pygame.locals import *
import tile_table
import mapfns

tile_chars = {'<':(0,0), '-':(1,0), '>':(2,0), '|':(3,0), '#':(3,1), '=': (3,1), '\\': (0,1),'/':(2,1),'O':(3,1)}
pygame.init()
screen = pygame.display.set_mode((432,522))
screen.fill((255,255,255))
table =  tile_table.load_tile_table('pacmantiles.png',18,18)
maparray = mapfns.mapchars(maptextfile = 'map3.txt')
tiles = [[],[]]
print(table)
'''for x, row in enumerate(table):
    for y, tile in enumerate(row):
        screen.blit(tile, (x*18, y*18))'''
for row in range(len(maparray)):
    for col in range(len(maparray[0])):
        tile_index = tile_chars[maparray[row][col]]
        screen.blit(table[tile_index[0]][tile_index[1]],(col*18,row*18))

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass            
