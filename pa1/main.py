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
        self.notAdded = True # bool - starting value means it hasn't been searched
        self.neighbors = []


# HELPER FUNCTIONS
start = []
goal = []

#for calculating h(x) - for the heuristic, use the "Manhattan distance" between 2 points
def distance(curr):
    # shortest possible distance while hitting all vertices
    distance = math.sqrt(2) * min(abs(curr.vertex[0]-goal[0]), abs(curr.vertex[1]-goal[1])) + max(abs(curr.vertex[0]-goal[0]), abs(curr.vertex[1]-goal[1])) - min(abs(curr.vertex[0]-goal[0]), abs(curr.vertex[1]-goal[1]))
    return distance

# for calculating g(x) - path cost so far from start to current node
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
    x, y = curr.vertex[0]-1, curr.vertex[1]-1

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

# main theta* update - finds if there is a shorter path thru a node's lineage
def line_of_sight(grandparent, grandchild, blocked): # TODO

    if grandparent is None:
        return False
    
    x0, y0 = grandparent.vertex[0], grandparent.vertex[1]
    x1, y1 = grandchild.vertex[0], grandchild.vertex[1]
    x_distance, y_distance = (x1 - x0), (y1 - y0)
    f = 0

    if y_distance < 0:
        y_distance = -y_distance
        grandparent.vertex[1] = -1
    else:
        grandparent.vertex[1] = 1
    if x_distance < 0:
        x_distance = -x_distance
        grandparent.vertex[0] = -1
    else:
        grandparent.vertex[0] = 1
    
    if x_distance >= y_distance:
        while x0 != x1:
            
            f += y_distance
            if f >= x_distance:
                print('one')
                print(x0+(0 if grandparent.vertex[0] == 1 else -1))
                print(y0+(0 if grandparent.vertex[1] == 1 else -1))
                if blocked[x0+(0 if grandparent.vertex[0] == 1 else -1)][y0+(0 if grandparent.vertex[1] == 1 else -1)]:
                    return False
                y0 += grandparent.vertex[1]
                f -= x_distance
            
            print('two')
            print(x0+(0 if grandparent.vertex[0] == 1 else -1))
            print(y0+(0 if grandparent.vertex[1] == 1 else -1))
            if f != 0 and blocked[x0+(0 if grandparent.vertex[0] == 1 else -1)][y0+(0 if grandparent.vertex[1] == 1 else -1)]:
                return False
            
            print('three')
            print(x0+(0 if grandparent.vertex[0] == 1 else -1))
            if y_distance == 0 and blocked[x0+(0 if grandparent.vertex[0] == 1 else -1)][y0] and [x0+(0 if grandparent.vertex[1] == 1 else -1)][y0-1]:
                return False
        
        x0 += grandparent.vertex[0]
    
    else:
        while y0 != y1:

            f += x_distance
            if f >= y_distance:
                print('four')
                print(x0+(0 if grandparent.vertex[0] == 1 else -1))
                print(y0+(0 if grandparent.vertex[1] == 1 else -1))
                if blocked[x0+(0 if grandparent.vertex[0] == 1 else -1)][y0+(0 if grandparent.vertex[1] == 1 else -1)]:
                    return False
                x0 += grandparent.vertex[0]
                f -= y_distance
            
            print('five')
            print(x0+(0 if grandparent.vertex[0] == 1 else -1))
            print(y0+(0 if grandparent.vertex[1] == 1 else -1))
            if f != 0 and blocked[x0+(0 if grandparent.vertex[0] == 1 else -1)][y0+(0 if grandparent.vertex[1] == 1 else -1)]:
                return False
            
            print('six')
            print(y0+(0 if grandparent.vertex[1] == 1 else -1))
            if x_distance == 0 and blocked[x0][y0+(0 if grandparent.vertex[1] == 1 else -1)] and [x0-1][y0+(0 if grandparent.vertex[1] == 1 else -1)]:
                return False
        
        y0 += grandparent.vertex[1]
    
    return True


# MAIN FUNCTION FOR BOTH A* AND THETA*
def main(func, size, blocked):

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
    start_node.h = distance(start_node)
    start_node.f = start_node.g + start_node.h
    start_node.neighbors = add_neighbors(start_node, grid)

    start_node.notAdded = False
    open_list.put((start_node.f, start_node.h, start_node)) # use h value for choosing priority between nodes with equal f values
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


            neighbor.h = distance(neighbor)
            neighbor.f = neighbor.g + neighbor.h
                    
            if neighbor.notAdded:
                neighbor.notAdded = False
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

        func = ['a', 'theta']
        main(func[1], size, blocked)
