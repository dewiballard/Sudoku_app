#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:39:22 2020

@author: dewiballard
"""
import numpy as np
from functools import reduce

example = np.array([[3,2,0, 0,0,0, 7,0,8],
                    [7,0,0, 1,0,0, 0,0,0],
                    [0,0,0, 6,0,0, 3,0,5],
                    
                    [0,4,5, 0,9,0, 0,0,0],
                    [0,0,0, 2,0,4, 0,0,0],
                    [0,0,0, 0,8,0, 9,5,0],
                    
                    [5,0,3, 0,0,2, 0,0,0],
                    [0,0,0, 0,0,7, 0,0,6],
                    [4,0,2, 0,0,0, 0,3,1]])

def solver(grid):
    numbers=np.arange(1,10)
    i,j = np.where(grid==0) 
    if (i.size==0):
        return(True,grid)
    else:
        i,j=i[0],j[0]    
        row = grid[i,:] 
        col = grid[:,j]
        sqr = grid[(int(i/3))*3:(3+(int(i/3))*3),(int(j/3))*3:(3+(int(j/3))*3)].reshape(9)
        values = np.setdiff1d(numbers,reduce(np.union1d,(row,col,sqr)))

        grid_temp = np.copy(grid) 

        for value in values:
            grid_temp[i,j] = value
            test = solver(grid_temp)
            if (test[0]):
                return(test)

        return(False,None)

print(solver(example))