import pickle
tuple = (0,'_')
highscore =[]
for i in range(10):
    highscore.append(tuple)

with open('data/highscore.txt', 'r+') as f:
    pickle.dump(highscore,f)
    print('yeah')
