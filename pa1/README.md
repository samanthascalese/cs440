# [CS440] Assignment 1 | Spring 2022
Contributors: `Sammi Scalese`, `Kelci Mensah`, `Maya Barathy`

<div align="center">

[Getting Started](#Getting-Started) • [Visualization Demo](#Visualization-Demo) </div>

### Table of Contents
- [Problem 1: Any-Angle Path Planning](#Problem-1:-Any-Angle-Path-Planning)
    - [Problem 1(a): Creating a Graphical User Interface](#Problem-1(a):-Creating-a-Graphical-User-Interface)
    - [Problem 1(b): Manual Computation of Shortest Path](#Problem-1(b):-Manual-Computation-of-Shortest-Path)
    - [Problem 1(c): Implementing A*](#)
    - [Problem 1(d): Implementing Theta*](#)
    - [Problem 1(e): Mathematical Proof of A*](#)

<hr>

### Getting Started
💋 all packages used within this assignment are available on the Rutgers University CS iLab machines.

### Visualization Demo
[ insert video demonsration here ]

## Problem 1: Any Angle Path Planning
### Problem 1(a): Creating a Graphical User Interface

```Text
Create an interface so as to create and visualize the 50 eight-neighbor grids you are going to use for the experiments. Your software should also be able to visualize: the start and the goal location, the path computed by an A*-family algorithm. Visualize the values h, g and ƒ computed by A*-family algorithms on each cell (e.g., after selecting with the mouse a specific cell, or after using the keyboard to specify which cell’s information to display). Use the images in this report from the traces of algorithms as a guide on how to design your visualization. 

Highlight in your report your visualization, its capabilities and what implemented for it.
(10 points)
```

### Problem 1(b): Manual Computation of Shortest Path
```Text
Read the chapter in your artificial intelligence textbook on uninformed and informed (heuris-
tic) search and then read the project description again. Make sure that you understand A*,

Theta* and the Bresenham line-drawing algorithm. Manually compute and show a shortest

grid path and a shortest any-angle path for the example search problem from Figure 7. Man-
ually compute and show traces of A* with the h-values from Equation 1 and Theta* with the

h-values h(s) = c(s, sgoal) for this example search problem, similar to Figures 3 and 5.
(5 points)
``` 

Shortest grid path = (1 + 1.4 + 1.4) = 3.8 units 
Shortest any angle path = (1.4 + 2.23) = 3.63 units 



### Problem 1(c): Implementing A*
(ii) Manually compute and show traces of A* with the h-values from Equation 1. \linebreak

Using A* the shortest path is from A4 to B3 to C2 to C1
A4 -> g(n) = 0, h(n) = 3.8, A4 = 0 + 3.8 = 3.8
B3 -> g(n) = 1.4, h(n) = 2.4, B3 = 1.4 + 2.4 = 3.8 
C2 -> g(n) = 1, h(n) = 2, C2 = 1 + 2 = 3
C1 -> g(n) 3.8, h(n) = 0, C1 = 0 + 3.8 = 3.8
The shortest path using A* = 3.8 + 3.8 + 3 + 3.8 = 14.4 units

(iii) Manually compute and show traces of Theta*. 
Using Theta* the shortest path is from A4 to B3 to C1
A4 -> g(n) = 0, h(n) = 1.4, A4 = 1.4
B3 -> g(n) = 1.4 h(n) = 2.24, B3 = 3.64
C1 -> g(n) = 2.24, h(n) = 0, C1 = 2.24

The shortest path using Theta* = 1.4 + 3.64 + 2.24 = 7.28 units 


c) Implement the A* algorithm for a given start and goal location for the grid environments. Describe in your report what you had to implement in order to have the A* algorithm working. \linebreak

d) Implement the Theta* algorithm for a given start and goal location for the grid environments. Describe in your report what you had to implement in order to have the Theta* algorithm working.\linebreak

e) Give a proof (=concise but rigorous argument) why A* with the h-values from equation 1 is guaranteed to find the shortest grid paths. \linebreak

When using A* we use the formula f(n) = g(n)+ h(n) to compute the shortest distance where g(n) is the distance from the initial state to node n which we can manually compute using addition and h(n) is the distance from the current node to the final state. The h values that we have obtained from Equation 1 provide us with the shortest path because it is admissible which means that it never overestimates the distance it will take to reach the goal state. Hence it is also optimally efficient and cost efficient. \linebreak

f) Implement your own binary heap and use it in both algorithms.Discuss your implementation in your final report. If you do execute this extra credit step, make sure that any run times you report in your answers below how your own implementation of a binary heap has influenced the running times.
