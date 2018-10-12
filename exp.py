#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:54:51 2018

@author: calbert
@author: guimard
"""

from pathologic import *
from search import *
import time
import os

def exp(filepath, search_mode):
    grid_init = readInstanceFile(filepath)
    init_state = State(grid_init)
    
    start_time = time.time()  
    
    problem = Pathologic(init_state)
    
    if search_mode == "BFSg":
        node = breadth_first_graph_search(problem)
    elif search_mode == "DFSg":
        node = depth_first_graph_search(problem)
    elif search_mode == "BFSt":
        node = breadth_first_tree_search(problem)
    elif search_mode == "DFSt":
        node = depth_first_tree_search(problem)
    else:
        raise ValueError("This search mode does not exist!")
    
    interval = time.time() - start_time
    print('\tTime : ' + str(interval))
    print('\tNB node explored : ' + str(problem.nb_explored_nodes))
    
    path = node.path()
    path.reverse()
    
    
    print('\tNumber of moves: ' + str(node.depth))

if __name__ == "__main__":
    search_modes = ["BFSg", "DFSg", "BFSt", "DFSt"]    
    print("Experiment with all instances and all uninformed search algorithms.")

    for instance in os.listdir("instances"):
        print("\n\nInstance " + instance + " :")
        for search_mode in search_modes:
            print("\n" + search_mode)
            exp("instances/" + instance, search_mode)