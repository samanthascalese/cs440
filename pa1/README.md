# [CS440] Assignment 1 | Spring 2022
Contributors: `Sammi Scalese`, `Kelci Mensah`, `Maya Barathy`

<div align="center">

[Getting Started](#Getting-Started) • [Quick Demo](#) </div>

### Table of Contents
- [Problem 1: Any-Angle Path Planning](#Problem-1-(a)---Creating-a-Graphical-User-Interface)
    - [Problem 1(a) - Creating a Graphical User Interface](#)
    - [Problem 1(b) - Manual Computation of Shortest Path](#)
    - [Problem 1(c) - Implementing A*](#)
    - [Problem 1(d) - Implementing Theta*](#)
    - [Problem 1(e) - Mathematical Proof of A*](#)

<hr>

### Getting Started
💋 all packages used within this assignment are available on the Rutgers University CS iLab machines.

### Quick Demo
[ insert video demonsration here ]

### Problem 1(a) - Creating a Graphical User Interface

```Text
Create an interface so as to create and visualize the 50 eight-neighbor grids you are going to use for the experiments. Your software should also be able to visualize: the start and the goal location, the path computed by an A*-family algorithm. Visualize the values h, g and ƒ computed by A*-family algorithms on each cell (e.g., after selecting with the mouse a specific cell, or after using the keyboard to specify which cell’s information to display). Use the images in this report from the traces of algorithms as a guide on how to design your visualization. Highlight in your report your visualization, its capabilities and what implemented for it.
(10 points)
```

### Problem 1(a) - Creating a Graphical User Interface
b) (i) Manually compute and show a shortest grid path and and a shortest any angle path for the example search problem from figure 7. \linebreak 

Shortest grid path = (1 + 1.4 + 1.4) = 3.8 units \linebreak
Shortest any angle path = (1.4 + 2.23) = 3.63 units \linebreak

(ii) Manually compute and show traces of A* with the h-values from Equation 1. \linebreak
Using A* the shortest path is 

(iii) Manually compute and show traces of Theta*. \linebreak

c) Implement the A* algorithm for a given start and goal location for the grid environments. Describe in your report what you had to implement in order to have the A* algorithm working. \linebreak

d) Implement the Theta* algorithm for a given start and goal location for the grid environments. Describe in your report what you had to implement in order to have the Theta* algorithm working.\linebreak

e) Give a proof (=concise but rigorous argument) why A* with the h-values from equation 1 is guaranteed to find the shortest grid paths. \linebreak

When using A* we use the formula f(n) = g(n)+ h(n) to compute the shortest distance where g(n) is the distance from the initial state to node n which we can manually compute using addition and h(n) is the distance from the current node to the final state. The h values that we have obtained from Equation 1 provide us with the shortest path because it is admissible which means that it never overestimates the distance it will take to reach the goal state. Hence it is also optimally efficient and cost efficient. \linebreak

f) Implement your own binary heap and use it in both algorithms.Discuss your implementation in your final report. If you do execute this extra credit step, make sure that any run times you report in your answers below how your own implementation of a binary heap has influenced the running times.
