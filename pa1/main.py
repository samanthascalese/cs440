import sys, math
from queue import PriorityQueue


# NODE OBJECT DEFINITION
class Node:

    def __init__(self, vertex) -> None:
        self.vertex = vertex # int array of size 2
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0.0
        self.parent = None
        self.notAdded = 1 # bool - starting value 1 mean it hasn't been searched
        self.neighbors = []


# HELPER FUNCTIONS
start = []
goal = []

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

# for calculating a* g(x) - path cost so far from start to current node
def cost(parent, curr):
    # straight across edge
    if (curr.vertex[0] == parent.vertex[0] or curr.vertex[1] == parent.vertex[1]):
        return 1.0
    else: # diagonal
        return math.sqrt(2)

# create the list of neighbors for a given node
# TODO: add stuff w/ blocked grid !!
def add_neighbors(curr, grid):

    neighbors = []
    x = curr.vertex[0]-1
    y = curr.vertex[1]-1

    # up 1
    if y > 0:
        neighbors.append(grid[x][y-1])
    # down 1
    if y < len(grid[0])-1:
        neighbors.append(grid[x][y+1])
    # left 1
    if x > 0:
        neighbors.append(grid[x-1][y])
    # right 1
    if x < len(grid)-1:
        neighbors.append(grid[x+1][y])
    # diagonal up & left
    if x > 0 and y > 0: 
        neighbors.append(grid[x-1][y-1])
    # diagonal up & right
    if x < len(grid)-1 and y > 0:
        neighbors.append(grid[x+1][y-1])
    # diagonal down & left
    if x > 0 and y < len(grid[0])-1:
        neighbors.append(grid[x-1][y+1])
    # diagonal down & right
    if x < len(grid)-1 and y < len(grid[0])-1:
        neighbors.append(grid[x+1][y+1])

    return neighbors

# files grid with default node objects holding the given vertex
# TODO: add stuff w/ blocked grid !!
def make_grid(size):

    grid = []

    for x in range(size[0]+1):
        grid.append([])
        for y in range(size[1]+1):
            node = Node([x+1,y+1])
            grid[x].append(node)

    return grid


# MAIN A* FUNCTION
def a_star(size, blocked):

    if start == goal:
        # testing
        print("Start node is goal node.")
        return

    grid = make_grid(size)

    # testing
    print("vertices:")
    for x in range(size[0]+1):
        print("(")
        for y in range(size[1]+1):
            print(grid[x][y].vertex)
        print(")")
    print()
    #testing

    open_list = PriorityQueue()
    closed_list = []

    start_node = grid[start[0]-1][start[1]-1]
    start_node.g = 0
    start_node.h = vertex_distance(start_node)
    start_node.f = start_node.g + start_node.h
    start_node.neighbors = add_neighbors(start_node, grid)

    start_node.notAdded = 0
    open_list.put((start_node.f, start_node.h, start_node)) # use h value for choosing priority between node with equal f values
    # testing
    print(f"Start{start_node.vertex} - f = {start_node.g} + {start_node.h} = {start_node.f}")

    while not open_list.empty():
        
        curr = open_list.get()[2] # gets the node itself, not the (key, value) pair
        closed_list.append(curr)
        # testing
        print()
        print(curr.vertex)

        # end of path
        if curr.vertex == goal:
            # testing
            print()
            print("Path is: ")
            for node in closed_list:
                print(node.vertex)
            return

        curr.neighbors = add_neighbors(curr, grid)
        for neighbor in curr.neighbors:

            path_cost = curr.g + cost(curr, neighbor)
            
            if path_cost < neighbor.g:
                    neighbor.parent = curr
                    neighbor.g = path_cost
                    neighbor.h = vertex_distance(neighbor)
                    neighbor.f = neighbor.g + neighbor.h
                    
                    if neighbor.notAdded:
                        neighbor.notAdded = 0
                        open_list.put((neighbor.f, neighbor.h, neighbor))
                        # testing
                        print(f"Node{neighbor.vertex} - f = {neighbor.g} + {neighbor.h} = {neighbor.f}")
                        

    print("No possible path.")
    return


# READ COMMAND LINE INPUT
if __name__ == "__main__":
    
    # opens command line input 1 as file "f", then auto-closes when done reading
    with open(sys.argv[1]) as f:
        
        line = f.readline()
        split = line.split()
        start = list(map(int, split)) # x = start[0], y = start[1]
        # testing
        print(f"start node: {start}")

        line = f.readline()
        split = line.split()
        goal = list(map(int, split)) # x = goal[0], y = goal[1]
        # testing
        print(f"goal node: {goal}")

        line = f.readline()
        split = line.split()
        size = list(map(int, split)) # x-length = size[0], y-length = size[1]
        # testing
        print(f"grid size: {size[0]} x {size[1]}")
        
        blocked = [[0 for y in range(size[1])] for x in range(size[0])]
        for line in f:
            split = line.split()
            cell = list(map(int, split)) # (x, y) = (cell[0]-1, cell[1]-1) b/c input starts at (1,1) not (0,0)
            blocked[cell[0]-1][cell[1]-1] = cell[2] # blocked? = cell[2]
        # testing
        print(f"blocked cells: {blocked}")

        a_star(size, blocked)


