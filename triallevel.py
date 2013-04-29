import ConfigParser

class level(object):
    def load_file(self,filename="level.map"):
        self.map=[]
        self.key={}
        parser=ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset=parser.get("level","map").split("\n")
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
            for map_x, c in enumerate(line)
                if tile(map_x, map_y)=='#' tile(map_x, map_y)=='=':
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
                else tile(map_x, map_y)=='/':
                   tile=1,3
        tile_image=tiles[tile[0]][tile[1]]
        image.blit(tile_image,(map_x*18,map_y*18))
    return image, overlays

                    
