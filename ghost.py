from math import sqrt
def reverse_lookup(d, v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError

class Ghost(object):
    directions = {'up': [0,1], 'left': [0,-1],'down': [0,-1],'right':[1,0]}
    def __init__(self, name = 'Ghost', position = [0,0], nextpos = [0,1], target = [-1,-1], vhat = [0,1], chase= False, speed =10):
        self.name = name
        self.position = position
        self.target = target
        self.chase = chase
        self.speed = speed
        self.vhat = vhat
        self.nextpos = nextpos
    def __str__(self):
        namestr = self.name.upper()
        posstr = 'position:  ' + str(self.position)
        targetstr = 'target:    ' + str(self.target) 
        speedstr = 'speed:     ' + str(self.speed)
        directionstr = 'direction: ' + str(reverse_lookup(self.directions, self.vhat))
        nextposstr = 'next pos:  ' + str(self.nextpos)
        chasestr = 'chase?     ' + str(self.chase)
        res = []
        res.append(namestr)
        res.append(posstr)
        res.append(targetstr)
        res.append(speedstr)
        res.append(directionstr)
        res.append(nextposstr)
        res.append(chasestr)
        
        return '\n'.join(res)
    def new_next_pos(self):
        possmoves = [[0,2],[-1,1],[0,0],[1,1]] 
        possmoves.remove(self.position)
        possdist = []
        for move in possmoves:
            possdist.append(sqrt((self.target[0] - move[0])**2 + (self.target[1] - move[1])**2))
        leastdistindex = 0
        for d in range(len(possdist)):
            if possdist[d] < possdist[leastdistindex]:
                leastdistindex = d 
        return possmoves[leastdistindex] 
    def make_move(self):
        temp_next_move = self.new_next_pos
        self.position = self.nextpos
        self.nextpos = temp_next_move
class Blinky(Ghost):
    def define_target(self,pacman):
        self.target = pacman.position
class Pinky(Ghost):
#Right now, just adding tiles, not pixels BTW
    def define_target(self,pacman):
        if pacman.vhat == directions['left']:
            self.target = [pacman.position[0] - 4, pacman.position[1]]
        elif pacman.vhat == directions['right']:
            self.target = [pacman.position[0] + 4, pacman.position[0]]
        elif pacman.vhat == directions['down']:
            self.target = [pacman.position[0], pacman.position[1] - 4]
        elif pacman.vhat == directions['up']:
            self.target = [pacman.position[0]-4, pacman.position[1] + 4] 
class Inky(Ghost):
    def define_target(self,pacman,blinky):
        offsettile = [0,0]
        if pacman.vhat == directions['left']:
            offsettile = [pacman.position[0] - 2, pacman.position[1]]
        elif pacman.vhat == directions['right']:
            offsettile = [pacman.position[0] + 2, pacman.position[0]]
        elif pacman.vhat == directions['down']:
            offsettile = [pacman.position[0], pacman.position[1] - 2]
        elif pacman.vhat == directions['up']:
            offsettile = [pacman.position[0]-2, pacman.position[1] + 2]
        self.target = [2*offsettile[0] - blinky.position[0], 2*offsettile[1] - blinky.position[1]]
class Clyde(Ghost):
    def define_target(self,pacman):
        dist = sqrt((self.position[0]-pacman.position[0])**2 + (self.position[1]-pacman.position[1])**2)
        if dist >= 8:
            self.target = pacman.position
        else:
            self.target = [-1,-29]
            #This should be the bottom left corner of the maze (I don't know what that is yet...]
        

Robert = Ghost('Robert')
print(Robert)
print(Robert.new_next_pos())

        
