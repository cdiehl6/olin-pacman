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
        possmoves = [[0,2],[1,1],[0,0],[-1,1]] 
        possmoves.remove(self.position)
        possdist = []
        for move in possmoves:
            possdist.append(sqrt((self.target[0] - move[0])**2 + (self.target[1] - move[1])**2))
        leastdistindex = 0
        for d in range(len(possdist)):
            if possdist[d] < possdist[leastdistindex]:
                leastdist = d        

Robert = Ghost('Robert')
print(Robert)
Robert.new_next_pos()
        
