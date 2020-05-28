#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:53:43 2020

@author: dewiballard
"""

import numpy as np
from functools import reduce

example = np.array([[0,12,0,4, 0,0,10,3, 2,11,8,9],
                    [0,10,6,0, 0,9,4,0, 0,0,1,0],
                    [0,2,3,0, 0,11,12,0, 7,0,0,0],
                    
                    [0,0,0,3, 0,1,7,12, 0,0,2,0],
                    [0,6,0,0, 0,0,0,0, 8,12,4,0],
                    [10,9,0,7, 2,0,0,0, 6,0,0,0],
                                        
                    [0,4,2,6, 0,5,0,9, 0,1,12,8],
                    [0,5,0,0, 4,0,0,0, 0,2,0,11],
                    [9,1,0,0, 0,10,0,7, 0,6,0,5],
                    
                    [0,0,1,0, 0,0,0,4, 0,0,6,12],
                    [12,11,0,0, 0,0,0,0, 0,0,0,0],
                    [0,3,9,2, 1,0,0,10, 0,0,0,4]])

def solver(grid):
    numbers=np.arange(1,13)
    i,j = np.where(grid==0) 
    if (i.size==0):
        return(True,grid)
    else:
        i,j=i[0],j[0]    
        row = grid[i,:] 
        col = grid[:,j]
        sqr = grid[(int(i/3))*3:(3+(int(i/3))*3),(int(j/4))*4:(4+(int(j/4))*4)].reshape(12)
        values = np.setdiff1d(numbers,reduce(np.union1d,(row,col,sqr)))
        grid_temp = np.copy(grid) 

        for value in values:
            grid_temp[i,j] = value
            test = solver(grid_temp)
            if (test[0]):
                return(test)

        return(False,None)

print(solver(example))