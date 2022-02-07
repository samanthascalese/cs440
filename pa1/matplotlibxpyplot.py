# -------------------------------------------------------------------------- #
#   H - Python Package Imports                           
# -------------------------------------------------------------------------- #
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import sys

# -------------------------------------------------------------------------- #
#   H - Read in Text File Input                    
# -------------------------------------------------------------------------- #
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

# -------------------------------------------------------------------------- #
#   H - Matrix Window Properties                            
# -------------------------------------------------------------------------- #
fig, ax = plt.subplots(figsize=(8,5), num="CS440 - Intro to Artificial Intelligence")


plt.title("Problem 1: Any-Angle Path Planning")
# plt.title('Click on plotted points for the g(), f(), and h() values!', fontsize=12) 

plt.gca().invert_yaxis()
plt.gca().xaxis.tick_top()
plt.gca().xaxis.set_tick_params(labeltop=True)

xaxis = np.zeros(gridsize[0]+1)
yaxis = np.zeros(gridsize[1]+1)
for i in range(gridsize[0]+1):
    xaxis[i] = i+1

for j in range(gridsize[1]+1):
    yaxis[j] = j+1

plt.xticks(np.arange(gridsize[0]+1), xaxis)
plt.yticks(np.arange(gridsize[1]+1), yaxis)

cmap = colors.ListedColormap(['white','steelblue']) # https://matplotlib.org/2.0.2/examples/color/named_colors.html
plt.pcolor(blockgrid[::],cmap=cmap, edgecolors='k', linewidths=0.5)

# -------------------------------------------------------------------------- #
#   H - Mapping Plot Points (w/ Interactive Information)                             
# -------------------------------------------------------------------------- #
# markingsize = 40

def on_pick(event):
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    # print ('Artist picked:', event.artist)
    # print ('{} Vertices Picked'.format(len(ind)))
    # print ('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
    # print ('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
    print ('Path Point:', x[ind[0]]+1, y[ind[0]]+1)

tolerance = 70 # number of points plotted

x_values = [startpoint[0]-1, goalpoint[0]-1]
y_values = [startpoint[1]-1, goalpoint[1]-1]
# plt.scatter(x_values, y_values, s=markingsize) 
plt.plot(x_values, y_values)



ax.plot(startpoint[0]-1, startpoint[1]-1, marker='o', picker=tolerance)
ax.plot(goalpoint[0]-1, goalpoint[1]-1, marker='o', picker=tolerance)

fig.canvas.callbacks.connect('pick_event', on_pick)

plt.show()