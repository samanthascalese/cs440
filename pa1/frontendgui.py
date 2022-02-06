# -------------------------------------------------------------------------- #
#   H - Package Import List                               
# -------------------------------------------------------------------------- #
import sys
import time
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from queue import PriorityQueue
from collections import deque

matrix = Tk()   # initialize tkinter matrix/grid

# -------------------------------------------------------------------------- #
#   H - Reading the Textfile                          
# -------------------------------------------------------------------------- #
if __name__ == "__main__":
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
        print(startpoint)

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
        
        print(blockgrid)

# -------------------------------------------------------------------------- #
#   H - Matrix/Grid Properties                              
# -------------------------------------------------------------------------- #
WIDTH = 650
ROWS = gridsize[0]
COLUMNS = gridsize[1]
grid = []

# -------------------------------------------------------------------------- #
#   H - Universal Window Properties                              
# -------------------------------------------------------------------------- #
matrix.title('Problem 1: Any-Angle Path Planning') # window title
matrix.maxsize(900, 900)
matrix.config(bg='#94B0DA') # set background color
font = ("System", 11)
userMenu = Frame(matrix, width=600, height=200, bg='#DCEDFF')
userMenu.grid(row=0, column=0, padx=10, pady=5)
canvas = Canvas(matrix, width=WIDTH, height=WIDTH, bg='#FFF')
canvas.grid(row=0, column=1, padx=10, pady=5) 

def make_grid(width, row, col):
    gapa = width // row
    gapb = width // col
    offset = 2

    if col > row:
        for i in range(row):
            grid.append([])
            for j in range(col):
                cell = pathExplorer(i, j, gapb, offset, row, col)
                grid[i].append(cell)
                # print(i, ", ", j)
    elif row >= col:
        for i in range(row):
            grid.append([])
            for j in range(col):
                cell = pathExplorer(i, j, gapa, offset, row, col)
                grid[i].append(cell)
                # print(i+","+j)
    
    return grid

# -------------------------------------------------------------------------- #
#   H - Mathematical Formulas                              
# -------------------------------------------------------------------------- #
def h(start, goal):     #heuristic
    return abs(start.row - goal.row) + abs(start.col - goal.col)

# -------------------------------------------------------------------------- #
#   H - Matrix/Grid Functions                          
# -------------------------------------------------------------------------- #
class pathExplorer:
    start_point = None
    end_point = None
    
    # __slots__ = ['button','row', 'col', 'width', 'neighbors', 'g', 'h', 'f',  
    #              'parent', 'start', 'end', 'barrier', 'clicked', 'total_rows']
    
    def __init__(self, row, col, width, offset, total_rows, total_columns):
        
        self.button = Button(canvas, command = lambda a=row, b=col: self.click(a, b), bg='white', bd=2, relief=RIDGE
        )
        
        self.row = row
        self.col = col
        self.width = width
        
        self.button.place(x=row * width + offset, y=col * width + offset, width=width, height=width)

        self.neighbors = []
        self.g = float('inf') 
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.start = False
        self.end = False
        self.barrier = False
        self.clicked = False
        self.total_rows = gridsize[0]
        self.total_cols = gridsize[1]
    
    def make_start(self):
        self.button.config(bg = "DarkOrange2")
        self.start = True
        self.clicked = True
        pathExplorer.start_point = (self.col, self.row)
        
    def make_end(self):
        self.button.config(bg = "#255957")
        self.end = True
        self.clicked = True
        pathExplorer.end_point = (self.col, self.row)
        
    def make_barrier(self):
        self.button.config(bg = "#757575")
        self.barrier = True
        self.clicked = True
        pathExplorer.b_point = (self.col, self.row)
        
    def reset(self):
        self.button.config(bg = "white")
        self.clicked = False
        
    def make_path(self):
        self.button.config(bg = "gold")
        
    def make_to_visit(self):
        self.button.config(bg = "pink")

    def make_backtracking(self):
        # self.button.config(bg = "SteelBlue1")
        self.button.config(bg = "#FFF")
        
    def make_open(self):
        # self.button.config(bg = "cornflower blue")
        self.button.config(bg = "#FFF")
        
    def make_closed(self):
        # self.button.config(bg = "LightSkyBlue2")
        self.button.config(bg = "#FFF")
        
    def disable(self):
        self.button.config(state=DISABLED)
    
    def enable(self):
        self.button.config(state=NORMAL)
    
    def click(self, row, col):
        if self.clicked == False:
            if not pathExplorer.start_point:   
                self.make_start()
            elif not pathExplorer.end_point:
                self.make_end()
            else :
                self.make_barrier()
        else:
            self.reset()
            if self.start == True:   
                self.start = False
                pathExplorer.start_point = None
            elif self.end == True:
                self.end = False
                pathExplorer.end_point = None
            else :
                self.barrier = False
    
    def update_neighbors(self, grid):
        self.neighbors = []

        # check neighbors a row down - if spot not outside grid and not barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier:
            self.neighbors.append(grid[self.row + 1][self.col]) # add spot to the neighbors

        # check neighbors a row up - if spot not outside grid and not barrier
        if self.row > 0 and not grid[self.row - 1][self.col].barrier:
            self.neighbors.append(grid[self.row - 1][self.col]) # add spot to the neighbors

        # check neighbors a col right - if spot not outside grid and not barrier
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].barrier:
            self.neighbors.append(grid[self.row][self.col + 1]) # add spot to the neighbors

        # check neighbors a col left - if spot not outside grid and not barrier
        if self.col > 0 and not grid[self.row][self.col - 1].barrier:
            self.neighbors.append(grid[self.row][self.col - 1]) # add spot to the neighbors

def pathHighlighter(spot, tickTime):
    current = spot
    while current.start == False:
        parent = current.parent
            
        parent.make_path()
        matrix.update_idletasks()
        time.sleep(tickTime)

        current = parent
        
# -------------------------------------------------------------------------- #
#   H - Path-Finding Algorithms                          
# -------------------------------------------------------------------------- #
def breadth_first(grid, tickTime):
    
    start = grid[pathExplorer.start_point[1]][pathExplorer.start_point[0]]
    end = grid[pathExplorer.end_point[1]][pathExplorer.end_point[0]]
    
    open_set = deque()
    
    open_set.append(start)
    visited_hash = {start}
    
    while len(open_set) > 0:
        current = open_set.popleft()
        
        # found end?
        if current == end:
            pathHighlighter(end, tickTime)
            
            # draw end and start again
            end.make_end()
            start.make_start()
            return
        
        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:
            
            if neighbor not in visited_hash:
                neighbor.parent = current
                visited_hash.add(neighbor)
                open_set.append(neighbor)
                neighbor.make_open()
                
        # draw updated grid with new open_set        
        matrix.update_idletasks()
        time.sleep(tickTime)
        
        if current != start:
            current.make_closed()
            
    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")

    return False

def a_star(grid, tickTime):

    count = 0
    start = grid[pathExplorer.start_point[1]][pathExplorer.start_point[0]]
    end = grid[pathExplorer.end_point[1]][pathExplorer.end_point[0]]
    
    # create open_set
    open_set = PriorityQueue()
    
    # add start in open_set with f_score = 0 and count as one item
    open_set.put((0, count, start))

    # put g_score for start to 0    
    start.g = 0
    
    # calculate f_score for start using heuristic function
    start.f = h(start, end)
    
    # create a dict to keep track of spots in open_set, can't check PriorityQueue
    open_set_hash = {start}
    
    # if open_set is empty - all possible spots are considered, path doesn't exist
    while not open_set.empty():
        
        # popping the spot with lowest f_score from open_set
        # if score the same, then whatever was inserted first - PriorityQueue
        # popping [2] - spot itself
        current = open_set.get()[2]
        # syncronise with dict
        open_set_hash.remove(current)
        
        # found end?
        if current == end:
            pathHighlighter(end, tickTime)
            
            # draw end and start again
            end.make_end()
            start.make_start()
            
            # enable UI frame
            for child in userMenu.winfo_children():
                child.configure(state='normal')
            return True
        
        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:
            
            # calculate g_score for every neighbor
            temp_g_score = current.g + 1
            
            # if new path through this neighbor better
            if temp_g_score < neighbor.g:
                
                # update g_score for this spot and keep track of new best path
                neighbor.parent = current
                neighbor.g = temp_g_score
                neighbor.f = temp_g_score + h(neighbor, end)
                
                if neighbor not in open_set_hash:
                    
                    # count the step
                    count += 1
                    
                    # add neighbor in open_set for consideration
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        # draw updated grid with new open_set        
        matrix.update_idletasks()
        time.sleep(tickTime)
        
        if current != start:
            current.make_closed()
            
    messagebox.showinfo("Uh oh :(", "There is no path" )    # path-finding failure

    return False

# -------------------------------------------------------------------------- #
#   H - Interactive Functions, Variables and Properties                          
# -------------------------------------------------------------------------- #
def Reset():
    global grid
        
    pathExplorer.start_point = None
    pathExplorer.end_point = None
    
    for row in grid:
        for cell in row:
            cell.reset()
            cell.neighbors = []
            cell.g = float('inf') 
            cell.h = 0
            cell.f = float('inf')
            cell.parent = None
            cell.start = False
            cell.end = False
            cell.barrier = False
            cell.enable()
            
def break_wall(current, new):
    if current.row == new.row:
        if current.col > new.col:
            # wall to the left from current
            wall = grid[current.row][current.col - 1]
        else:
            # wall to the right
            wall = grid[current.row][current.col + 1]
    else:
        if current.row > new.row:
            # wall above
            wall = grid[current.row - 1][current.col]
        else:
            # wall below
            wall = grid[current.row + 1][current.col]
    # break wall
    wall.reset()
    wall.barrier = False

def pressStart():
    global grid

    # -------------------------------------------------------------------------- #
    # MAKE START AND GOAL GIVEN VERTICES

    if not pathExplorer.start_point:
        current = grid[startpoint[0]-1][2]
        if current.end == False:
            current.make_start()

    if not pathExplorer.end_point:
        current = grid[startpoint[0]-1][0]
        if current.start == False:
            current.make_end()

    start = grid[pathExplorer.start_point[0]][pathExplorer.start_point[1]]
    end = grid[pathExplorer.end_point[0]][pathExplorer.end_point[1]]

    # if not grid: return
    # if not pathExplorer.start_point or not pathExplorer.end_point: 
    #     messagebox.showinfo("No start/end", "Place starting and ending points")
    #     return

    # -------------------------------------------------------------------------- #
    # MAKE BARRIERS
    
    for r in range(0, gridsize[1]):
        for c in range(0, gridsize[0]):
            print(blockgrid[r][c], r, c)
            if blockgrid[r][c] == 1:
                current = grid[c][r]
                current.make_barrier()  
    
    # -------------------------------------------------------------------------- #
    # UPDATING NEIGHBORS LIST
    for row in grid:
        for spot in row:
            spot.neighbors = []
            spot.g = float('inf') 
            spot.h = 0
            spot.f = float('inf')
            spot.parent = None
            spot.update_neighbors(grid)
            if spot.clicked == False:
                spot.reset()
            spot.disable() # disable buttons in the grid for running algorithm
    
    # disable UI frame for running algorithm
    for child in userMenu.winfo_children():
        child.configure(state='disable')
    
    # -------------------------------------------------------------------------- #
    # MATCHING ALGORITHM CHOICE
    if algMenu.get() == 'A*':
        a_star(grid, 0.08) #speedscale
    elif algMenu.get() == 'Breadth-First Search':
        breadth_first(grid, 0.05)     #speedscale
        
    # enable buttons in the grid
    for row in grid:
        for spot in row:
            spot.enable()
    
    for child in userMenu.winfo_children():
        child.configure(state='normal') # enable frame

# -------------------------------------------------------------------------- #
#   H - User Botton Menu                          
# -------------------------------------------------------------------------- #
selected_alg = StringVar()
selected_bld = StringVar()

algMenu = ttk.Combobox(userMenu, textvariable=selected_alg, 
                       values=['A*', 'Breadth-First Search'], font = font)
algMenu.grid(row=3, column=0, padx=5, pady=(20, 5), sticky=W)
algMenu.current(0)
Button(userMenu, text='Start Search', command=pressStart, font = ("System", 14,),
       bg='#EE6352').grid(row=5, column=0, padx=5, pady=(10, 10))

Button(userMenu, text='Clear Grid', command=Reset, font = ("System", 14),
       bg='white').grid(row=6, column=0, padx=5, pady=(20, 30))


grid = make_grid(WIDTH, ROWS, COLUMNS)
matrix.mainloop()