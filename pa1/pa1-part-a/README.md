# [CS440] Assignment 1 | Spring 2022
Contributors: `Sammi Scalese`, `Kelci Mensah`, `Maya Barathy`

<div align="center">

[Getting Started](#Getting-Started) • [Testing the Code](#Testing-the-Code) </div>

<hr>

### Getting Started
> *All packages used within this assignment are available on the Rutgers University CS iLab machines.

1. Unzip the file and ensure that it contains the directory `test` and the following files: `README.md`, `assignment_one.py`,  `Assignment 1 Part A - Report.pdf`, and `path images`.

2. Log into `https://weblogin.cs.rutgers.edu/guacamole-1.3.0/` and select any of the iLab machine domains. 

3. Ensure that the file `assignment_one.py` and the `test` directory are in the same home directory.

4. Open the start menu and run the program `Xcfe Terminal`.

5. Locate to the directory containing both the python program file and the `test` directory by typing `cd [directory name]`. You should be able to see both items. If you only see the test text files, you've gone too far in and need to return at least one directory.

### Testing the Code
1. To properly display the test cases, only one text file should be in the test directory at the time. Placing multiple text file inputs into the test directory will print individual information for each file but will only display the corresponding graph for the last file in the directory.

2. To run the code for some test input "icecreamshop.txt" and display its path for the A* algorithm, place that text file into the `test` enter the following command:
```Python
Python3 assignment_one.py test/ a
```

3. In order to display a different graph or test a different algorithm, you must close the `matplotlib` grid window that opens upon running the file. All information in the terminal corresponds to the graph and displays the following information:
- start goal
- end goal
- shortest path
- heuristic values f, g, and h

3. To run the code for some different test input "localmall.txt" and display its path for the Theta* algorithm, place that text file into the `test` enter the following command:
```Python
Python3 assignment_one.py test/ theta
```

4. The `Matplotlib` library offers the user controls in order to navigate the grid and zoom into node (points). In the case that it is still difficult to see, we have implemeneted a way for the user to click a specfici point and the terminal will report its location. In this way, you can find the direct information for the point and cross-check the values.