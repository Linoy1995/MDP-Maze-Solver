import numpy as np
import cv2
from PIL import Image
import numpy as np
from typing import Dict, List, Tuple
#from maze import Maze, Cell, Agent
import turtle

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
cellDim = 70
#Grid 10X10
CellRowsAmount=10   #number of cells' rows
CellColAmount=10    #number of cells' columns
    
class Cell():
    def __init__(self, x: int, y: int):
        #if False= no wall, True=has wall
        self.walls: Dict[str, bool] = {'N': False, 'S': False, 'E': False, 'W': False}


class Maze():   #a class that map the maze

    cellCenter = (35,35)
    
    def __init__(self): #get a maze picture
        cell_center_to_border = {'N': (0, -34), 'S': (0, 34), 'E': (34, 0), 'W': (-34, 0)}    #dictionary for calculate borders of cell
        self.img = cv2.imread("newMaze.jpg")
        self.maze=self.img[:,:,0]
        self.maze = np.array(self.maze)       
        height, width ,shape =self.img.shape  #height=width=700
        self.cells = [[Cell(x, y) for x in range(CellRowsAmount)] for y in range(CellColAmount)] #Grid of 10X10 Cell()
        for r in range(width):
            for c in range(height):
                if self.maze[r,c] < 150.0:
                    self.maze[r,c]=0.0
                else:
                    self.maze[r,c]=255.0

        #check if a cell has walls
        for x in range(CellRowsAmount):
            for y in range(CellColAmount):
                    if self.maze[x*(cellDim)+self.cellCenter[0]+cell_center_to_border['N'][1]][y*(cellDim)+self.cellCenter[1]]==0:
                        self.cells[x][y].walls['N']= True 
                    if self.maze[x*(cellDim)+self.cellCenter[0]+cell_center_to_border['S'][1]][y*(cellDim)+self.cellCenter[1]]==0:
                        self.cells[x][y].walls['S']= True
                    if self.maze[x*cellDim+self.cellCenter[0]][y*(cellDim)+self.cellCenter[1]+cell_center_to_border['W'][0]]==0:
                        self.cells[x][y].walls['W']= True
                    if self.maze[x*cellDim+self.cellCenter[0]][y*(cellDim)+self.cellCenter[1]+cell_center_to_border['E'][0]]==0:
                        self.cells[x][y].walls['E']= True




class Agent(turtle.Turtle):
    pen=turtle.Turtle()
    def __init__(self):
        self.pen.penup()
        self.pen.speed(0) #fastest
        self.pen.goto(-349+maze.cellCenter[0], 315)
        self.pen.shape("square")
        self.pen.shapesize(1,1)
        self.pen.right(-90)
        self.pen.color("red")
        self.pen.pendown()
        self.pen.speed(1)   #slowest speed
        self.agentCellNum=0
          
    def move(self, direction):
            self.pen.speed(0) #fastest
            if direction == 0:  #UP
              self.agentCellNum-=10
              self.pen.fd(70)

            if direction == 1:  #RIGHT
              self.pen.right(90)
              self.agentCellNum+=1
              self.pen.fd(70)
              self.pen.right(-90)

            if direction == 2:  #DOWN
                self.agentCellNum+=10
                self.pen.backward(70)

            if direction == 3:  #LEFT
                self.agentCellNum-=1
                self.pen.left(90)
                self.pen.fd(70)
                self.pen.right(90)
            self.pen.speed(6)   #slow speed

            wn.update()

          
    def getAgentCellNum(self):
        return self.agentCellNum

            

class mazeEnv():    #define the enviornment of the maze
    def __init__(self):
        self.statesList=[CellRowsAmount,CellColAmount]   #a list of states in maze [10,10]
        self.states_amount=np.prod(self.statesList) #total size of states
        self.actions_amount=4
        self.grid = np.arange(self.states_amount).reshape(self.statesList) #create numpy array from statesList
        it = np.nditer(self.grid, flags=['multi_index'])         #allow comfortable access to indexes
      
        self.actionsOptions = {
            UP : [UP, RIGHT, LEFT],
            DOWN : [DOWN, RIGHT, LEFT],
            LEFT : [LEFT, UP, DOWN],
            RIGHT : [RIGHT, DOWN, UP]
        }
        
        self.probabilities=(0.8,0.1,0.1)   #forward, right, left
        
        P={}    #dictionary that tells for each cell how to move from a given state by an action
        #P ={next_state, reward}
   
        while not it.finished:
            s = it.iterindex        #current state
            y, x = it.multi_index   #get indexes

            P[s] = {a : [] for a in range(self.actions_amount)} #initial dictionary with 4 keys of actions for a current state
            is_done = lambda s: s == (self.states_amount - 1)   #check if the state is the goal
            reward = 1.0 if is_done(s) else 0.0

            # The goal
            if is_done(s):
                P[s][UP] = [(s, reward)]
                P[s][RIGHT] = [(s, reward)]
                P[s][DOWN] = [(s, reward)]
                P[s][LEFT] = [(s, reward)]
            
            # on the way to the goal
            #if wall or border: Reward=-1,  
            else:
                next_state_up = s if y == 0 or maze.cells[y][x].walls['N']==True else s - CellColAmount
                reward=-1.0 if y == 0 or maze.cells[y][x].walls['N']==True else -0.04
                P[s][UP] = [(next_state_up, reward)]

                next_state_right = s if x == (CellColAmount - 1) or maze.cells[y][x].walls['E']==True else s + 1
                reward=-1.0 if x == (CellColAmount - 1) or maze.cells[y][x].walls['E']==True else -0.04
                P[s][RIGHT] = [(next_state_right, reward)]

                next_state_down = s if y == (CellRowsAmount - 1) or maze.cells[y][x].walls['S']==True else s + CellColAmount
                reward=-1.0 if y == (CellRowsAmount - 1) or maze.cells[y][x].walls['S']==True else -0.04
                P[s][DOWN] = [(next_state_down, reward)]

                next_state_left = s if x == 0 or maze.cells[y][x].walls['W']==True else s - 1
                reward=-1.0 if x == 0 or maze.cells[y][x].walls['W']==True else -0.04
                P[s][LEFT] = [(next_state_left, reward)]

            it.iternext()
        self.P = P
    
    
    def applyAction(self, s1, a):
          if a in self.actionsOptions:
            res = {}

            #For each possible action ac from action a
            for i in range(len(self.actionsOptions[a])):    #actionsOptions[a]=the possible action of agent to walk from current direction
                action = self.actionsOptions[a][i]          #action= get an option.  i=0 equals to keep going forward. i=1,2 left or right ****of the agent***
                [(next_state, reward)] = self.P[s1][action]      #find next state from the current if the action will be applied
                res[action] = {'state' : next_state, 'prob' : self.probabilities[i]}    #get the probability to reach the next state. i=0=forward=0.8 prob
            return res   #return a dictionary with the next state option and its probability
    
        
    
    def setup_maze(self, level):    #maze window
        wn = turtle.Screen()
        wn.bgcolor("white")
        wn.title("A Maze Game")
        wn.setup(750,750)
        wn.bgcolor("white")
        wn.bgpic('newMaze.gif')  
        wn.update()
        return wn
    
    def moveAgent(self, Reshaped_Grid_Policy, agent):   #move the agent
        currentCellNum=agent.getAgentCellNum()
        while currentCellNum < self.states_amount-1:
            foundCell=False
            it = np.nditer(self.grid, flags=['multi_index'])         #allow comfortable access to indexes  
            while not it.finished and foundCell==False:
                s = it.iterindex        #current state
                y, x = it.multi_index   #get indexes
                if currentCellNum==s:
                    direction=Reshaped_Grid_Policy[y,x]
                    agent.move(direction)
                    currentCellNum=agent.getAgentCellNum()
                    foundCell=True
                else:
                    it.iternext()
   

def one_step_lookahead(V, a, poss, s, env, discount_factor):
        #check the state of the next actions value
        v=0
        [(next_state, curr_reward)] = env.P[s][a]
        for r in poss:
            [(next_state, reward)] = env.P[s][r]
            prob=poss[r]['prob']
            v+=(prob*V[next_state])
        v = v*discount_factor+curr_reward

        return v

    
def value_iteration(env, epsilon=0.0001, discount_factor=0.99):
        
    #start with inital value function and intial policy
    value = np.zeros(env.states_amount)
    policy = np.zeros([env.states_amount, env.actions_amount])
    #while not the optimal policy
    while True:
      #for stopping condition
        delta = 0
        
    	#loop over state space
        for state in range(env.states_amount):
            max_val = float('-inf')
            max_action = None    			
            val_Arr=np.zeros(env.actions_amount)
    		#loop over possible actions and check the maximum value to apply policy
            for action in range (env.actions_amount):
                    possible_actions=env.applyAction(state, action)     #a dictionary with the next state option and its probability according to last step
                # if action in possible_actions:
                    #apply bellman eqn to get actions values
                    val = one_step_lookahead(value, action, possible_actions,state, env, discount_factor)
                    if val>max_val:
                        max_val=val
                        max_action=action
                        max_action=np.int64(max_action)
                        val_Arr[action]=max_val
            
            delta = max(delta, abs(max_val - value[state]))
            value[state]=max_val
            policy[state]=np.eye(env.actions_amount)[max_action]
            
        if delta<epsilon:   #convergence
            break

    	
    return policy, value


maze=Maze()     #setting the maze grid
mazeEnv=mazeEnv()
policy, value = value_iteration(mazeEnv)
agent=Agent()
wn=mazeEnv.setup_maze(maze)

# print("Policy Probability Distribution:")
# print(policy)
# print("")

print("Reshaped Grid Policy (0=up, 1=right, 2=down, 3=left):")
Reshaped_Grid_Policy=np.reshape(np.argmax(policy, axis=1), mazeEnv.statesList)
print(Reshaped_Grid_Policy)
print("")
print("Value Function:")
print(value)
print("")

print("Reshaped Grid Value Function:")
print(value.reshape(mazeEnv.statesList))
print("")
mazeEnv.moveAgent(Reshaped_Grid_Policy, agent)
wn.mainloop()
turtle.bye()
