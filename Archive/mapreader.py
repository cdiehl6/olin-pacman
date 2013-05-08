#Open the file and read the entire file
with open('map.txt', 'r') as f:
    read_data = f.readlines() 
#get just the map from the read data

read_data = read_data[2:]
for index in range(len(read_data)):
    read_data[index] = read_data[index][4:]
    print(read_data[index])

is_move_poss = [[0 for c in range(len(read_data[1]))] for r in range(len(read_data))]
for r in range(len(read_data)):
    for c in range(len(read_data[r])):
        if read_data[r][c] == '#':
            is_move_poss[r][c] = 1
    print(is_move_poss[r])
print(len(is_move_poss))
print(len(is_move_poss[0]))   
