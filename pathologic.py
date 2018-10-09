# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *


#################
# Problem class #
#################
class Pathologic(Problem):
    
    def __init__(self, initial, goal=None):
        self.initial = initial 
        self.goal = goal
        

    def successor(self, state):
        i,j = state.get_pos()
        if j+1 < state.nbc and state.grid[i][j+1] in ['0','_']:
            newState = state.clone()
            newState.move('right',i,j)
            yield ('right',newState)
        
        if j-1 >= 0 and state.grid[i][j-1] in ['0','_']:
            newState = state.clone()
            newState.move('left',i,j)
            yield ('left',newState)
            
        if i+1 < state.nbr and state.grid[i+1][j] in ['0','_']:
            newState = state.clone()
            newState.move('down',i,j)
            yield ('down',newState)
            
        if i-1 >= 0 and state.grid[i-1][j] in ['0','_']:
            newState = state.clone()
            newState.move('up',i,j)
            yield ('up',newState)
        
    def goal_test(self, state):
        for i in range(0,state.nbr):
            for j in range(0,state.nbc):
                if state.grid[i][j]=='_':
                    return False
        return True

###############
# State class #
###############

class State:
    def __init__(self, grid):
        self.nbr = len(grid) # nb of row
        self.nbc = len(grid[0])
        self.grid = grid

    def __str__(self):
        s = ""
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j]) + " "
            s = s.rstrip()
            if i < self.nbr - 1:
                s = s + '\n'
        return s
    
    def clone(self):
        new_grid = [[0 for i in range(self.nbc)] for j in range(self.nbr)]
        for i in range (0,self.nbr):
            for j in range(0,self.nbc):
                new_grid[i][j] = self.grid[i][j]
        return State(new_grid)

    def set_init_pos(self):
        for i in range(0,self.nbr):
            for j in range(0,self.nbc):
                if self.grid[i][j]=='$':
                    self.pos = (i,j)
                
    def move(self, direction, x, y):
        self.grid[x][y] = 'x'
        if direction == 'left':
            self.grid[x][y-1] = '$'
            self.pos = (x,y-1)
        elif direction == 'right':
            self.grid[x][y+1] = '$'
            self.pos = (x,y+1)
        elif direction == 'up':
            self.grid[x-1][y] = '$'
            self.pos = (x-1,y)
        elif direction == 'down':
            self.grid[x+1][y] = '$'
            self.pos = (x+1,y)
        else:
            raise ValueError('Impossible to move in this direction.')
    def get_pos(self):
        return self.pos

######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [line.replace(" ","").rstrip('\n') for line in open(filename)]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(0, m)] for i in range(0, n)]
    return grid_init


#####################
# Launch the search #
#####################

grid_init = readInstanceFile(sys.argv[1])
init_state = State(grid_init)
init_state.set_init_pos()

problem = Pathologic(init_state)

# example of bfs graph search
node = breadth_first_graph_search(problem)

# example of print
path = node.path()
path.reverse()



print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()