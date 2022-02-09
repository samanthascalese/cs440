# -------------------------------------------------------------------------- #
#   Python Package Imports                           
# -------------------------------------------------------------------------- #
import os, sys, math
from queue import PriorityQueue
from cupshelpers import setPPDPageSize
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np

# FOR TESTING
MIN_TESTING = True
MAX_TESTING = True

# NODE OBJECT DEFINITION
class Node:

    def __init__(self, vertex) -> None:
        self.vertex = vertex # int array of size 2
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0.0
        self.parent = None
        self.notAdded = True # bool - starting value means it hasn't been searched
        self.newNeighbor = False # bool - starting value means it hasn't added any new neighbors to the open_list
        self.neighbors = []

start = []
goal = []
correctpath = []

# -------------------------------------------------------------------------- #
#   HELPER FUNCTIONS                           
# -------------------------------------------------------------------------- #
#for calculating a* h(x) - for the heuristic, use the "Manhattan distance" between 2 points
def vertex_distance(curr):
    # shortest possible distance while hitting all vertices
    distance = math.sqrt(2) * min(abs(curr.vertex[0]-goal[0]), abs(curr.vertex[1]-goal[1])) + max(abs(curr.vertex[0]-goal[0]), abs(curr.vertex[1]-goal[1])) - min(abs(curr.vertex[0]-goal[0]), abs(curr.vertex[1]-goal[1]))
    return distance

# for calculating theta* h(x) - for the heuristic, use distance line between 2 points
def line_distance(curr):
    # shortest possible distance
    distance = math.sqrt(pow(goal[0]-curr.vertex[0], 2) + pow(goal[1]-curr.vertex[1], 2))
    return distance

# for calculating g(x) - path cost so far from start to current node
def cost(parent, curr):
    # straight across edge
    if (curr.vertex[0] == parent.vertex[0] or curr.vertex[1] == parent.vertex[1]):
        return 1.0
    else: # diagonal
        return math.sqrt(2)

# create the list of neighbors for a given node
def add_neighbors(curr, grid, blocked):

    neighbors = []
    x, y = curr.vertex[0]-1, curr.vertex[1]-1

    # UP/DOWN & LEFT/RIGHT LINES BLOCKED
    # case 1: neighbor edge is between two blocked cells
    # case 2: neighbor edge is between a blocked cell and lower bound
    # case 3: neighbor edge is between a blocked cell and upper bound

    # up 1
    if y > 0:
        if not ((x == 0 and blocked[x][y-1]) # case 2
            or (x == len(grid)-1 and blocked[x-1][y-1]) # case 3
            or (x > 0 and blocked[x-1][y-1] and blocked[x][y-1])): # case 1
            neighbors.append(grid[x][y-1])
    
    # down 1
    if y < len(grid[0])-1:
        if not ((x == 0 and blocked[x][y]) # case 2
            or (x == len(grid)-1 and blocked[x-1][y]) # case 3
            or (x > 0 and blocked[x-1][y] and blocked[x][y])): # case 1
                neighbors.append(grid[x][y+1])
    
    # left 1
    if x > 0:
        if not ((y == 0 and blocked[x-1][y]) # case 2
            or (y == len(grid[0])-1 and blocked[x-1][y-1]) # case 3
            or (y > 0 and blocked[x-1][y-1] and blocked[x-1][y])): # case 1
                neighbors.append(grid[x-1][y])
    
    # right 1
    if x < len(grid)-1:
        if not ((y == 0 and blocked[x][y]) # case 2
            or (y == len(grid[0])-1 and blocked[x][y-1]) # case 3
            or (y > 0 and blocked[x][y-1] and blocked[x][y])): # case 1
                neighbors.append(grid[x+1][y])
    
    # DIAGONAL LINES BLOCKED
    # case 4: neighbor edge crosses through a blocked cell
    
    # diagonal up & left
    if x > 0 and y > 0: 
        if not blocked[x-1][y-1]:
            neighbors.append(grid[x-1][y-1])
    
    # diagonal up & right
    if x < len(grid)-1 and y > 0:
        if not blocked[x][y-1]:
            neighbors.append(grid[x+1][y-1])
    
    # diagonal down & left
    if x > 0 and y < len(grid[0])-1:
        if not blocked[x-1][y]:
            neighbors.append(grid[x-1][y+1])
    
    # diagonal down & right
    if x < len(grid)-1 and y < len(grid[0])-1:
        if not blocked[x][y]:
            neighbors.append(grid[x+1][y+1])

    return neighbors

# files grid with default node objects holding the given vertex
def make_grid(size):

    grid = []

    for x in range(size[0]+1):
        grid.append([])
        for y in range(size[1]+1):
            node = Node([x+1,y+1])
            grid[x].append(node)

    return grid

# main theta* update - finds if there is a shorter path thru a node's lineage
# TODO: THIS IS A MASSIVE MESS PLS IGNORE :(
def line_of_sight(grandparent, grandchild, blocked_list): # TODO

    if grandparent is None:
        return False

    x0, y0 = grandparent.vertex[0], grandparent.vertex[1]
    x1, y1 = grandchild.vertex[0], grandchild.vertex[1]
    f = 0
    dy, dx = (y1 - y0), (x1 - x0)

    if dy < 0:
        dy = -dy
        sy = -1
    else:
        sy = 1
    
    if dx < 0:
        dx = -dx
        sx = -1
    else:
        sx = 1

    if dx >= dy:
        while x0 != x1:
            f = f + dy
            if f >= dx:
                if (x0 + ((sx-1)//2), y0 + ((sy-1)//2)) in blocked_list:
                    return False
                y0 = y0 + sy
                f = f - dx
            
            if f != 0 and (x0 + ((sx-1)//2), y0 + ((sy-1)//2)) in blocked_list:
                return False
            
            if dy == 0 and (x0 + ((sx-1)//2), y0) in blocked_list and (x0 + ((sx-1)//2), y0-1) in blocked_list:
                return False
            
            x0 = x0 + sx
    else:
        while y0 != y1:
            f = f + dx
            if f >= dy:
                if (x0 + ((sx-1)//2), y0 + ((sy-1)//2)) in blocked_list:
                    return False
                x0 = x0 + sx
                f = f - dy
            
            if f != 0 and (x0 + ((sx-1)//2), y0 + ((sy-1)//2)) in blocked_list:
                return False

            if dx == 0 and (x0, y0 + ((sy-1)//2)) in blocked_list and (x0-1, y0 + ((sy-1)//2)) in blocked_list:
                return False
            
            y0 = y0 + sy
    
    return True

# -------------------------------------------------------------------------- #
#   MAIN FUNCTION FOR BOTH A* AND THETA*                         
# -------------------------------------------------------------------------- #
def main(func, size, blocked, correctpath):

    if start == goal:
        print("Start node is goal node.")
        return

    grid = make_grid(size)

    # testing
    # if (MAX_TESTING):
    #     print("vertices:")
    #     for x in range(size[0]+1):
    #         print("(")
    #         for y in range(size[1]+1):
    #             print(grid[x][y].vertex)
    #         print(")")
    #     print()

    open_list = PriorityQueue()
    closed_list = []

    start_node = grid[start[0]-1][start[1]-1]
    start_node.g = 0
    if func == 'a':
        start_node.h = vertex_distance(start_node)
    else:
        start_node.h = line_distance(start_node)
    start_node.f = start_node.g + start_node.h
    start_node.neighbors = add_neighbors(start_node, grid, blocked)

    start_node.notAdded = False
    open_list.put((start_node.f, start_node.h, id(start_node), start_node)) # use h value for choosing priority between nodes with equal f values
    # testing
    if (MAX_TESTING):
        print(f"Start{start_node.vertex} - f = {start_node.g} + {start_node.h} = {start_node.f}")

    while not open_list.empty():
        
        curr = open_list.get()[3] # gets the node itself, not the (key, value) pair
        # testing
        if (MAX_TESTING):
            print()
            print(curr.vertex)

        # end of path
        if curr.vertex == goal:
            closed_list.append(curr)
            # testing
            if (MIN_TESTING):
                print()
                print("Path is: ")
                for node in closed_list:
                    print(node.vertex)
                    correctpath.append(node.vertex)
                    # correctpath +=1
                    # print(correctpath)
                    

            return correctpath

        curr.neighbors = add_neighbors(curr, grid, blocked)
        for neighbor in curr.neighbors:

            # THETA* FUNCTION - path 2
            if func == 'theta' and line_of_sight(curr.parent, neighbor, blocked):
            
                path_cost = curr.parent.g + cost(curr.parent, neighbor)
                if path_cost < neighbor.g:
                    neighbor.parent = curr.parent
                    neighbor.g = path_cost
        
            # A* FUNCTION & THETA* FUNCTION - path 1
            else:
            
                path_cost = curr.g + cost(curr, neighbor)
                if path_cost < neighbor.g:
                    neighbor.parent = curr
                    neighbor.g = path_cost

            if func == 'a':
                neighbor.h = vertex_distance(neighbor)
            else:
                neighbor.h = line_distance(neighbor)
            neighbor.f = neighbor.g + neighbor.h
                    
            if neighbor.notAdded:
                curr.newNeighbor = True
                neighbor.notAdded = False
                open_list.put((neighbor.f, neighbor.h, id(neighbor), neighbor))
                # testing
                if (MAX_TESTING):
                    print(f"Node{neighbor.vertex} - f = {neighbor.g} + {neighbor.h} = {neighbor.f}")

        if curr.newNeighbor:
            closed_list.append(curr)


    print("No possible path.")
    return

# -------------------------------------------------------------------------- #
#   READ COMMAND LINE INPUT                         
# -------------------------------------------------------------------------- #
if __name__ == "__main__":
    
    # opens directory given in command line and runs all files
    for file in os.listdir(sys.argv[1]):
        # opens file "f", then auto-closes when done reading
        with open(os.path.join(sys.argv[1], file)) as f:
        
            line = f.readline()
            split = line.split()
            start = list(map(int, split)) # x = start[0], y = start[1]
            # testing
            if (MIN_TESTING):
                print(f"start node: {start}")

            line = f.readline()
            split = line.split()
            goal = list(map(int, split)) # x = goal[0], y = goal[1]
            # testing
            if (MIN_TESTING):
                print(f"goal node: {goal}")

            line = f.readline()
            split = line.split()
            size = list(map(int, split)) # x-length = size[0], y-length = size[1]
            # testing
            if (MIN_TESTING):
                print(f"grid size: {size[0]} x {size[1]}")
            
            blocked = [[0 for y in range(size[1])] for x in range(size[0])]
            for line in f:
                split = line.split()
                cell = list(map(int, split)) # (x, y) = (cell[0]-1, cell[1]-1) b/c input starts at (1,1) not (0,0)
                blocked[cell[0]-1][cell[1]-1] = cell[2] # blocked? = cell[2]
            # testing
            if (MIN_TESTING):
                print(f"blocked cells: {blocked}")

            func = ['a', 'theta']
            correctpath = main(func[1], size, blocked, correctpath).copy()
        
        print("- - - - - - - - - - - - - - - - - -")

# -------------------------------------------------------------------------- #
#   Matrix Window Properties                            
# -------------------------------------------------------------------------- #
fig, ax = plt.subplots(figsize=(10,8), num="CS440 - Intro to Artificial Intelligence")

plt.title("Problem 1: Any-Angle Path Planning")
# plt.title('Click on plotted points for the g(), f(), and h() values!', fontsize=12) 

plt.gca().invert_yaxis()
plt.gca().xaxis.tick_top()
plt.gca().xaxis.set_tick_params(labeltop=True)

column = size[0] + 1    # x axis
row = size[1] + 1   # y axis

xaxis = np.zeros(column)
yaxis = np.zeros(row)

for i in range(column):
    xaxis[i] = i+1

for j in range(row):
    yaxis[j] = j+1

plt.xticks(np.arange(column), xaxis)
plt.yticks(np.arange(row), yaxis)
ax.set_xticklabels(xaxis.astype(int))
ax.set_yticklabels(yaxis.astype(int))

cmap = colors.ListedColormap(['white','#CBEFB6']) # https://matplotlib.org/2.0.2/examples/color/named_colors.html
plt.pcolor(blocked[::],cmap=cmap, edgecolors='k', linewidths=0.5)

# -------------------------------------------------------------------------- #
#   Mapping Plot Points (w/ Interactive Information)                             
# -------------------------------------------------------------------------- #
# markingsize = 40

# TODO: make it so the map is the right size? also add h, g, f printouts

def on_pick(event): # TODO
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    # print ('Artist picked:', event.artist)
    # print ('{} Vertices Picked'.format(len(ind)))
    # print ('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
    # print ('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    print ('You are currently looking at vertex: [', y[ind[0]]+1,",",x[ind[0]]+1,"]")

tolerance = 70 # area of clickability for interactive event "on_pick"

# ax.plot(goal[1]-1, goal[0]-1, marker='o', picker=tolerance, color="#137547")    # goal is always green


fig.canvas.callbacks.connect('pick_event', on_pick)
 
pavedpath = np.array(correctpath)

xx, yy = pavedpath.T

for i in range(len(pavedpath)):

    if i == 0:
        plt.scatter(pavedpath[0,1]-1, pavedpath[0,0]-1, color="#000000")    # start is always black
    elif i == len(pavedpath)-1:
        plt.scatter(pavedpath[len(pavedpath)-1,1]-1, pavedpath[len(pavedpath)-1,0]-1, color="#000000")
    else:
        plt.scatter(pavedpath[i,1]-1, pavedpath[i,0]-1)

    plt.pause(0.45) 

    if (i == len(pavedpath)-1):
        ax.plot(yy-1,xx-1, picker=tolerance, color="#635D5C")   

plt.show()