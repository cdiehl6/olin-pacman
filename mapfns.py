from math import floor

import os, sys

#Given a position in pixels, return the box that the position is in. 
def pos_to_box(position = (0,0), boxsize=18):
    boxx = int(floor(position[0]/boxsize))
    boxy = int(floor(position[1]/boxsize))
    return (boxx, boxy)

#Given a box position, return the position of the center of the box
def box_to_pos(box = (0,0), boxsize=18):
    posx = int(box[0]*boxsize - floor(boxsize/2))
    posy = int(box[1]*boxsize - floor(boxsize/2))
    return (posx, posy)

#Return a table where each line of the table is a row of the map.txt map
def mapchars(maptextfile = 'map.txt'):
    maptextfile = os.path.join(os.path.dirname(sys.argv[0]),'data',maptextfile)
     #Open the file and read the entire file
    with open(maptextfile, 'r') as f:
        read_data = f.readlines()
 
    #get just the map from the read data
    read_data = read_data[2:31] 
    for index in range(len(read_data)):
        read_data[index] = read_data[index][4:-1]

    return read_data

#Return a table whose values reflect wether or not a box is a legal move
def mapgen(maptextfile = 'map.txt'):
    #Open the file and read the entire file
    maptextfile = os.path.join(os.path.dirname(sys.argv[0]),'data',maptextfile)
    with open(maptextfile, 'r') as f:
        read_data = f.readlines() 
    #get just the map from the read data

    #Get just the map
    read_data = read_data[2:31]
    for index in range(len(read_data)):
        read_data[index] = read_data[index][4:-1]
     
    #Fill in is_move_poss.
    is_move_poss = [[0 for c in range(len(read_data[1]))] for r in range(len(read_data))]
    for r in range(len(read_data)):
        for c in range(len(read_data[r])):
            #Everyone can move here (draw a normal dot)
            if read_data[r][c] == '#':
                is_move_poss[r][c] = 1
            #Only ghosts can move here (The house)
            elif read_data[r][c] == '=':
                is_move_poss[r][c] = 0.5
            #Draw a super dot here
            elif read_data[r][c] == 'O':
                is_move_poss[r][c] = 2
    return is_move_poss


