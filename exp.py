#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:54:51 2018

@author: calbert
"""

from pathologic import *
from search import *
import time

def exp():
    grid_init = readInstanceFile("instances/i10")
    init_state = State(grid_init)
    
    start_time = time.time()  
    
    problem = Pathologic(init_state)
    
    # example of bfs graph search
    node = depth_first_graph_search(problem)
    
    interval = time.time() - start_time  
    print('Time : ' + str(interval))
    print('NB node explored : ' + str(problem.nbNodesExplored))
    
    # example of print
    path = node.path()
    path.reverse()
    
    
    print('Number of moves: ' + str(node.depth))
    '''for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format
        print()'''
        
exp()