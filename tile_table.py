import pygame 

#Create a table with all the tiles that will go in our map. Width and height are the width and height of the tiles.
def load_tile_table(filename, width, height):
    #Import the image, and get the image width and height.
    image=pygame.image.load(filename).convert()
    image_width, image_height=image.get_size()
    #Get subsurfaces of the original image that are the tiles.
    tiles= []
    for tile_x in range(0, image_width/width):
        line=[]
        tiles.append(line)
        for tile_y in range(0, image_height/height):
            rect=(tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    #Return the final tile table.
    return tiles

#If name is main, print out each tile once
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
            

