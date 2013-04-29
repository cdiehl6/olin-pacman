import pygame
#from pygame.locals

def load_table_tile(filename, width, height):
    image=pygame.image.load(filename).convert()
    image_width, image_height=image.get_size()
    tile_table=[]
    for tile_x in range(0, image_width/width):
        line=[]
        tile_table.append(line)
        for tile_y in range(0, image_height/height)
            rect=(tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table
def __name__=='__main__':
    pygame.int()
    screen=pygame.display.set_mode((450,522))
    screen.fill((255,255,255))
    table=load_tile_table("pacmantiles.png",72,36)
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile,(x*18,y*18))
    pygame.display.flip()
    while pygame.event.wait(().type !=pygame.locals.QUIT:
    
