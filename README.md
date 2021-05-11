# MDP-Maze-Solver

![maze_mdp](https://user-images.githubusercontent.com/49640652/117788708-4cc46800-b250-11eb-9d12-51031e60f18b.jpg)


In this project I solved a maze by using the MDP algorithm and a policy that works according to value iteration.
The idea of the solution is to find the best probability of the agent choosing any action from any location on the maze board.

The size of the maze image is 700X700 pixels. The image is divided into a grid with 100 cells (a 10X10 matrix), so that each cell is 70X70 pixels in size.
For each cell a test is performed that marks the walls that surround it and stores the information accordingly in a dictionary-type structure.

## Project structure
The project is based on two main classes called Maze and mazeEnv
#### Maze class 
The class translates an image into a 10X10 matrix 
and paints each cell accordingly: if there is a wall - the cell will be painted black, otherwise - white.
In addition, under this class the walls are marked for each cell.

#### mazeEnv
The class defines the maze environment. It creates a structure that will hold for each possible situation the next possible action, the probability of making a step, the state the agent can reach, and the reward that the agent will receive for performing the action.

#### Additional classes the project consists:
Cell- represents a cell in the grid.  Holds a dictionary-type structure while the key is the direction of the wall (North, East, West, South), and the values are True or False for each key.
 
Agent- represents an agent object which tries to find his way out of the maze

#### Optimal Policy
In order to implement the MDP algorithm and to find out the most optimal path, I created a method that finds the optimal policy called value iteration.
As a result, for each state the best probability action will be chosen.
The method relies on Bellman equation:
![Bellman equation](https://user-images.githubusercontent.com/49640652/117789554-20f5b200-b251-11eb-9dc8-595861ad67f5.jpg)

Consequently, for each state the value for each possible action is calculated (by applying the one_step_lookahead action), and the highest value is selected.
Thus, for each iteration the policy will be updated by the best value found.
The meaning of the policy is to direct the agent to the next optimal cell depending on the state it is at the present moment, so the agent will start moving after the policy creation is complete.
