import sys

if __name__ == "__main__":
    
    # opens command line input 1 as file "f", then auto-closes when done reading
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
        start = list(map(int, split)) # x = start[0], y = start[1]
        print(start)

        line = f.readline()
        split = line.split()
        goal = list(map(int, split)) # x = goal[0], y = goal[1]
        print(goal)

        line = f.readline()
        split = line.split()
        size = list(map(int, split)) # x-length = size[0], y-length = size[1]
        print(size)
        
        grid = [[0 for x in range(size[0])] for y in range(size[1])]
        print(grid)

        for line in f:
            split = line.split()
            cell = list(map(int, split)) # (x, y) = (cell[1]-1, cell[0]-1) b/c input starts at (1,1) not (0,0)
            grid[cell[1]-1][cell[0]-1] = cell[2] # blocked? = cell[2]
            print(cell)
        
        print(grid)
