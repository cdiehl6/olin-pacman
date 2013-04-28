import pygame
import pygame.locals
import ConfigParser

def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    print(image_width)
    print(image_height)
    tile_table = []
    for tile_x in range(0, image_width/width):
        print('hi')
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            print(rect)
            line.append(image.subsurface(rect))
    return tile_table

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((432,522))
    screen.fill((255, 255, 255))
    table = load_tile_table("pacmantiles.png", 18, 18)
    print (list (enumerate(table)))
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*18, y*18))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass

class Level(object):
   def load_file(self,filename="level.map"):
        self.map=[]
        self.key={}
        parser=ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset=parser.get("Level","map").split("\n")
        print('self.tileset')
        if len(section)==1:
            desc=dict(parser.items(section))
            self.key[section]=desc
        self.width=len(self.map[1])
        self.height=len(self.map)
   def get_tile(self,x,y):
        try:
            char=self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}
   def tile(self,x,y):
        return self.get_tile(x,y)
   def render(self):
        wall =self.tile
        tiles=MAP_CHACHE[self.tileset]
        image=pygame.Surface((self.width*18, self.height*18))
        overlays={}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if tile(map_x, map_y)=='#' or tile(map_x, map_y)=='=':
                    tile=1,4
                elif tile(map_x, map_y)=='<':
                   tile=2,1
                elif tile(map_x, map_y)=='>':
                   tile=2,3
                elif tile(map_x, map_y)=='-':
                   tile=1,2
                elif tile(map_x, map_y)=='|':
                   tile=2,4
                elif tile(map_x, map_y)=='\\':
                   tile=1,1
                else:  #tile(map_x, map_y)=='/'
                   tile=1,3
        tile_image=tiles[tile[0]][tile[1]]
        image.blit(tile_image,(map_x*18,map_y*18))
        return image, overlays
if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    MAP_TILE_WIDTH = 18
    MAP_TILE_HEIGHT = 18
    MAP_CACHE = {'pacmantiles.png': load_tile_table('pacmantiles.png', MAP_TILE_WIDTH,MAP_TILE_HEIGHT)}

    level = Level()
    level.load_file('level.map')

    clock = pygame.time.Clock()

    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    pygame.display.flip()
game_over = False
while not game_over:

    # XXX draw all the objects here

    overlays.draw(screen)
    pygame.display.flip()
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            game_over = True
        elif event.type == pygame.locals.KEYDOWN:
            pressed_key = event.key
