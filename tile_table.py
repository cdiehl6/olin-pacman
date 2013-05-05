import pygame 
#from pygame.locals

def load_tile_table(filename, width, height):
    image=pygame.image.load(filename).convert()
    image_width, image_height=image.get_size()
    tiles= []
    for tile_x in range(0, image_width/width):
        line=[]
        tiles.append(line)
        for tile_y in range(0, image_height/height):
            rect=(tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))

    return tiles

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((468,504))
    screen.fill((255,255,255))
    table=load_tile_table("pacmantiles.png",72,36)
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*32, y*24))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
            

