# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:42:31 2020

@author: pm11lms
"""

from grids import getGrid as gg
import numpy as np
import time

def convert_nums():
    global grid
    for y in range(0,len(grid)):
        for x in range (0,len(grid[0])):
            if grid[y][x] == 10:
                grid[y][x] = "A"
            elif grid[y][x] == 11:
                grid[y][x] = "B"
            elif grid[y][x] == 12:
                grid[y][x] = "C"
            elif grid[y][x] == 13:
                grid[y][x] = "D"
            elif grid[y][x] == 14:
                grid[y][x] = "E"
            elif grid[y][x] == 15:
                grid[y][x] = "F"
            elif grid[y][x] == 16:
                grid[y][x] = "G"
                

def get_grid_dim():
    global grid
    y = len(grid)
    if y == 16:
        yBox = 4
    if y == 9 or y == 12:
        yBox = 3
    if y == 6:
        yBox = 2
    if y == 4:
        yBox = 2
        
    x = len(grid[0])
    if x == 16 or x == 12:
        xBox = 4
    if x == 9 or x == 6:
        xBox = 3
    if x == 4:
        xBox = 2
        
    return x, y, xBox, yBox


def find_Low_Constraints():
    global grid
    global dim # 0: xSize, 1: ySize, 2: xBox, 3: 
    pos = (-1,-1)
    minimum_count =  dim[0] # max number of values
    nums = dim[2] * dim[3]
    for y in range(0, dim[1]):
        for x in range(0, dim[0]):
            if grid[y][x] == 0:
                count = 0
                for n in range(1,nums+1):
                    if possible_move(y, x, n):
                        count += 1
                if count < minimum_count:
                    minimum_count = count 
                    pos = (x,y)
    return pos

                
                
                        

def possible_move(y,x,n):
    global grid
    global dim # 0: xSize, 1: ySize, 2: xBox, 3: yBox
    
    for i in range(0,dim[1]):
        if grid[y][i] == n:
            return False
    for i in range(0,dim[0]):
        if grid[i][x] == n:
            return False

    x0 = (x//dim[2])*dim[2]
    y0 = (y//dim[3])*dim[3]
    for j in range(0,dim[3]):
        for i in range(0,dim[2]):
            if grid[y0+j][x0+i] == n:
                return False  
    return True


def solve():
    global grid
    global sFound
    global dim # 0: xSize, 1: ySize, 2: xBox, 3: yBox
    nums = dim[2] * dim[3]
    for y in range(dim[1]):
        for x in range(dim[0]):
            if grid[y][x] == 0:
                for n in range(1,nums+1):
                    if possible_move(y, x, n):
                        grid[y][x] = n
                        solve()
                        if sFound == True:
                            return
                        grid[y][x] = 0
                return 
    sFound = True

def solver():
    global grid
    global sFound
    global dim # 0: xSize, 1: ySize, 2: xBox, 3: yBox
    nums = dim[2] * dim[3]
    x,y = find_Low_Constraints()
    if x != -1 and y != -1:
        for n in range(1,nums+1):
            if possible_move(y, x, n):
                grid[y][x] = n
                solver()
                if sFound == True:
                    return
                grid[y][x] = 0
        return 
    else:
        sFound = True 
        return
            
Time_taken = []
for i in range(10):
    grid = gg(5)
    sFound = False
    dim = get_grid_dim()
    start = time.clock()
    solver()
    end = time.clock()
    Time_taken.append(end-start)
    
if dim[0] == 12 or dim [0] == 16:
    convert_nums()
print(np.matrix(grid))

aTime = sum(Time_taken)/len(Time_taken)
print("Average time taken to solve: " + str(aTime))
