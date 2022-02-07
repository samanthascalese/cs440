from matplotlib import pyplot as plt
from matplotlib import colors
import sys

with open(sys.argv[1]) as f:
        # NOTES:
        # - - - - - - - - - - - -
        # line = f.readline()
        #   - reads the full line of file "f" as a single string
        #   - line is a str
        #
        # split = line.split()
        #   - splits the single string into chucks using whitespace
        #     as the delimiter
        #   - split is a str array
        # 
        # property = list(map(int, property))
        #   - maps the str array "split" into an int array "property"
        #   - property (i.e. start, goal, etc.) is an int array
        
        line = f.readline()
        split = line.split()
        startpoint = list(map(int, split)) # x = start[0], y = start[1]
        # print(startpoint)

        line = f.readline()
        split = line.split()
        goalpoint = list(map(int, split)) # x = goal[0], y = goal[1]
        # print(goalpoint)

        line = f.readline()
        split = line.split()
        gridsize = list(map(int, split)) # x-length = size[0], y-length = size[1]
        # print(gridsize)
        
        blockgrid = [[0 for x in range(gridsize[0])] for y in range(gridsize[1])]
        # print(blockgrid)

        for line in f:
            split = line.split()
            cell = list(map(int, split)) # (x, y) = (cell[1]-1, cell[0]-1) b/c input starts at (1,1) not (0,0)
            blockgrid[cell[1]-1][cell[0]-1] = cell[2] # blocked? = cell[2]
            # print(cell)
        
        # print(blockgrid)

cmap = colors.ListedColormap(['white','dimgrey'])
plt.figure(figsize=(gridsize[0],gridsize[1]), num="CS440 - Intro to Artificial Intelligence")
plt.title('Problem 1: Any-Angle Path Planning')
plt.pcolor(blockgrid[::-1],cmap=cmap, edgecolors='k', linewidths=1)
plt.show()