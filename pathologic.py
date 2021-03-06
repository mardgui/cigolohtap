# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>, Simon Calbert <simon.calbert@student.uclouvain.be>, Quentin Guimard <quentin.guimard@student.uclouvain.be>'''
from search import *


#################
# Problem class #
#################
class Pathologic(Problem):
    """An extension of the Problem class, suited for the Pathologic problem."""
    
    def __init__(self, initial, goal=None):
        """Constructor of the Pathologic class, with the same parameters as the Problem class."""
        self.initial = initial # Initial state of the problem
        self.goal = goal # Never used

        # Fully scans the grid only once at the beggining to get the position of the player and the circles
        self.initial.set_init_pos()
        self.initial.set_init_circles()
        
        self.nb_explored_nodes = 0

    def successor(self, state):
        """Successor method of the Pathologic class, with the same parameters as the Problem class."""
        self.nb_explored_nodes += 1
        (i, j) = state.pos
        
        # Check for neighbor circles
        neigbors_circles = []
        if j + 1 < state.nbc and state.grid[i][j + 1] == '_':
            neigbors_circles.append([i, j + 1]) 
                
        if j > 0 and state.grid[i][j - 1] == '_':
            neigbors_circles.append([i, j - 1]) 
            
        if i + 1 < state.nbr and state.grid[i + 1][j] == '_':
            neigbors_circles.append([i + 1, j]) 
            
        if i > 0 and state.grid[i - 1][j] == '_':
            neigbors_circles.append([i - 1, j]) 
        
        # Check for deadlocks next to neighbor circles    
        for k in range(0, len(neigbors_circles)):
            pos = neigbors_circles[k]
            x = pos[0]
            y = pos[1]
            nb_access = 0
            if y + 1 < state.nbc and state.grid[x][y + 1] in {'0', '_'}:
                nb_access += 1
            if y > 0 and state.grid[x][y - 1] in {'0', '_'}:
                nb_access += 1
            if x + 1 < state.nbr and state.grid[x + 1][y] in {'0', '_'}:
                nb_access += 1  
            if x > 0 and state.grid[x - 1][y] in {'0', '_'}:
                nb_access += 1  
            if nb_access == 0 and state.nb_circles > 1: 
                return
                yield


        ## Check if the map is split into 2 parts and so if the problem is stil solvable
        # Check for an horizontal split
        horizontal = True
        for k in range(0, state.nbc):
            if k != j and state.grid[i][k] in {'0', '_'}:
                if (i > 0 and state.grid[i - 1][k] in {'0', '_'}) or (i + 1 < state.nbr and state.grid[i + 1][k] in {'0', '_'}):
                    horizontal = False
                    break
        # Check if there are circles in the top and in the bottom part
        if horizontal == True:
            up = False
            down = False
            for k in range(0, state.nb_circles):
                circle = state.circles[k]
                if circle[0] - i < 0:
                    up = True
                elif circle[0] - i > 0:
                    down = True
                if up == True and down == True:
                   return
                   yield 
                   
        # Check for a vertical split
        vertical = True
        for k in range(0, state.nbr):
            if k != i and state.grid[k][j] in {'0', '_'}:
                if (j > 0 and state.grid[k][j - 1] in {'0', '_'}) or (j + 1 < state.nbc and state.grid[k][j + 1] in {'0', '_'}):
                    vertical = False
                    break
        # Check if there are circles in the left and in the right part
        if vertical == True:
            left = False
            right = False
            for k in range(0, state.nb_circles):
                circle = state.circles[k]
                if circle[1] - j < 0:
                    left = True
                elif circle[1] - j > 0:
                    right = True
                if left == True and right == True:
                   return
                   yield
            
            
        ## Look which actions are possible
        if j + 1 < state.nbc and state.grid[i][j + 1] in {'0', '_'}:
            newState = state.clone()
            newState.move('right')
            yield ('right', newState)
            
        if j - 1 >= 0 and state.grid[i][j - 1] in {'0', '_'}:
            newState = state.clone()
            newState.move('left')
            yield ('left', newState)
                
        if i + 1 < state.nbr and state.grid[i + 1][j] in {'0', '_'}:
            newState = state.clone()
            newState.move('down')
            yield ('down', newState)
                
        if i - 1 >= 0 and state.grid[i - 1][j] in {'0', '_'}:
            newState = state.clone()
            newState.move('up')
            yield ('up', newState)
        
    def goal_test(self, state):
        """Goal_test method of the Pathologic class, with the same parameters as the Problem class."""
        # This method has been extremely simplified thanks to a counter of the number of circles left in the grid
        return state.nb_circles == 0

###############
# State class #
###############

class State:
    """The state class, containing the grid of the game."""

    def __init__(self, grid):
        """Constructor of the State class, with the grid as the only parameter."""
        self.nbr = len(grid) # Number of rows
        self.nbc = len(grid[0]) # Number of columns
        self.grid = grid
        self.pos = None # Position of the player
        self.nb_circles = 0 # Number of circles left in the grid
        self.circles = [] # Positions of the circles in the grid

    def __str__(self):
        """Method used for displaying the grid, automatically called whenever print(State) is used."""
        s = ""
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j]) + " "
            s = s.rstrip()
            if i < self.nbr - 1:
                s = s + '\n'
        return s
    
    def clone(self):
        """Clone method of State, allowing a deep copy of the state class."""
        new_grid = [[0 for i in range(self.nbc)] for j in range(self.nbr)]
        for i in range (0, self.nbr):
            for j in range(0, self.nbc):
                new_grid[i][j] = self.grid[i][j]
        new_state = State(new_grid)
        new_state.pos = self.pos
        new_state.nb_circles = self.nb_circles
        new_state.circles = list(self.circles)
        return new_state

    def set_init_pos(self):
        """Set_init_pos scans the grid and stores the position of the player in self.pos."""
        is_looping = True
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                if self.grid[i][j] == '$':
                    self.pos = (i, j)
                    is_looping = False
                    break
            if not is_looping:
                break
            
    def set_init_circles(self):
        """Set_init_pos scans the grid and stores the number of circles in self.nb_circles , as well as their positions in self.circles."""
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                if self.grid[i][j] == '_':
                    self.nb_circles += 1
                    self.circles.append((i, j))
                
    def move(self, direction):
        """Move modifies the grid according to the chosen direction. The player is moved and is replaced by a cross.
           The variables self.pos, self.nb_circles and self.nb_circles are updated if needed."""
        (x,y) = self.pos
        self.grid[x][y] = 'x'

        if direction == 'left':
            if self.grid[x][y - 1] == '_':
                self.nb_circles -= 1
                self.circles.remove((x, y - 1))
            self.grid[x][y - 1] = '$'
            self.pos = (x, y - 1)

        elif direction == 'right':
            if self.grid[x][y + 1] == '_':
                self.nb_circles -= 1
                self.circles.remove((x, y + 1))
            self.grid[x][y + 1] = '$'
            self.pos = (x, y + 1)

        elif direction == 'up':
            if self.grid[x - 1][y] == '_':
                self.nb_circles -= 1
                self.circles.remove((x - 1, y))
            self.grid[x - 1][y] = '$'
            self.pos = (x - 1, y)

        elif direction == 'down':
            if self.grid[x + 1][y] == '_':
                self.nb_circles -= 1
                self.circles.remove((x + 1, y))
            self.grid[x + 1][y] = '$'
            self.pos = (x + 1, y)

        else:
            raise ValueError('Impossible to move in this direction.')

######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [line.replace(" ", "").rstrip('\n') for line in open(filename)]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(0, m)] for i in range(0, n)]
    return grid_init


#####################
# Launch the search #
#####################

if __name__ == "__main__":

    grid_init = readInstanceFile(sys.argv[1])
    init_state = State(grid_init)

    problem = Pathologic(init_state)

    # Using bfs tree search
    node = breadth_first_tree_search(problem)

    path = node.path()
    path.reverse()


    print('Number of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format
        print()
