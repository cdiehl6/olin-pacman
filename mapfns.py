from math import floor
def pos_to_box(position = (0,0), boxsize=18):
    boxx = int(floor(position[0]/boxsize))
    boxy = int(floor(position[1]/boxsize))
    return (boxx, boxy)

def box_to_pos(box = (0,0), boxsize=18):
    posx = int(box[0]*boxsize - floor(boxsize/2))
    posy = int(box[1]*boxsize - floor(boxsize/2))
    return (posx, posy)

def mapgen(maptextfile = 'map.txt'):
    #Open the file and read the entire file
    with open(maptextfile, 'r') as f:
        read_data = f.readlines() 
    #get just the map from the read data

    read_data = read_data[2:31]
    for index in range(len(read_data)):
        read_data[index] = read_data[index][4:]
        
    is_move_poss = [[0 for c in range(len(read_data[1]))] for r in range(len(read_data))]
    for r in range(len(read_data)):
        for c in range(len(read_data[r])):
            if read_data[r][c] == '#':
                is_move_poss[r][c] = 1
            elif read_data[r][c] == 'O':
                is_move_poss[r][c] = 2
    return is_move_poss
