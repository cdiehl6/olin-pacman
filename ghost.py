from math import sqrt
#get the key in the dictionary from the value
def reverse_lookup(d, v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError
#Defines the generic ghost object
class Ghost(object):
    #Dictionary to go from direction to direction unit vector
    directions = {'up': [0,1], 'left': [0,-1],'down': [0,-1],'right':[1,0]}
    def __init__(self, name = 'Ghost', position = [0,0], nextpos = [0,1], target = [-1,-1], vhat = [0,1], chase= False, speed =10):
	#Initialize ghost parameters
        self.name = name
        self.position = position
        self.target = target
        self.chase = chase
        self.speed = speed
        self.vhat = vhat
        self.nextpos = nextpos
    def __str__(self):
	#Print out Ghosty stuff
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
	#Get all possible moves 2 moves in the futre in the order up, left, down, right
        possmoves = [[0,2],[-1,1],[0,0],[1,1]] 
	#Remve the current position (the ghost cannot reverse direction)
        possmoves.remove(self.position)
	#Find the distance from each possible move to the target tile
        possdist = []
        for move in possmoves:
            possdist.append(sqrt((self.target[0] - move[0])**2 + (self.target[1] - move[1])**2))
	#Find the move that is closest (if two are the same, the order is: up, left, down right)
        leastdistindex = 0
        for d in range(len(possdist)):
            if possdist[d] < possdist[leastdistindex]:
                leastdistindex = d 
	#Return the new next position
        return possmoves[leastdistindex] 
	
    def make_move(self):
	#Get the new next move
        temp_next_move = self.new_next_pos
	#Make the current positon the old next position
        self.position = self.nextpos
	#make the next position, the new next move
        self.nextpos = temp_next_move

#Create the specific ghosts
class Blinky(Ghost):
	#Blinky's target is pacman
    def define_target(self,pacman):
        self.target = pacman.position
class Pinky(Ghost):
	#Pinky's target is 4 tiles offset in the direction pacman is moving, except when pacman is moving up. Then it is 4 tiles up and 4 to the left.

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
#I don't even know how to describe this target tile. The dossier says this: "To determine Inky's target, we must first establish an intermediate offset two tiles in front of Pac-Man in the direction he is moving (represented by the tile bracketed in green above). Now imagine drawing a vector from the center of the red ghost's current tile to the center of the offset tile, then double the vector length by extending it out just as far again beyond the offset tile.
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
    #Clyde targets pacman when pacman is more than 8 squares away, and the bottom left corner when pacman is closer
    def define_target(self,pacman):
        #get the distance from Clyde to pacman
        dist = sqrt((self.position[0]-pacman.position[0])**2 + (self.position[1]-pacman.position[1])**2)
        #set the target
        if dist >= 8:
            self.target = pacman.position
        else:
            self.target = [-1,-1]
            #This should be the bottom left corner of the maze (I don't know what that is yet]
        

Robert = Ghost('Robert')
print(Robert)
print(Robert.new_next_pos())

        
