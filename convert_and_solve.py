# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:56:08 2020

@author: pm11lms
"""


from grids import getGrid as gg
from Sudoku_s import solveGrid as sg

'''
grid = gg(5)
d = dict()
i = 1
gridList = []
for y in grid:
    for x in y:
        s = "cell" + str(i)
        d.update({s: x})
        i += 1
'''

def DictToList(d):
    gl = []
    for key, value in d.items():
        gl.append(value)
    return gl


def ListToGrid(lst):
    rows = []
    if len(lst) == 16:
        for y in range(0,4): 
            i = []
            for x in range(0,4):
                num = y * 4 + x
                i.append(lst[num])
            rows.append(i)
        return rows
    
    elif len(lst) == 36:
        for y in range(0,6): 
            i = []
            for x in range(0,6):
                num = y * 6 + x
                i.append(lst[num])
            rows.append(i)
        return rows

    elif len(lst) == 81:
        for y in range(0,9): 
            i = []
            for x in range(0,9):
                num = y * 9 + x
                i.append(lst[num])
            rows.append(i)
        return rows
    
    elif len(lst) == 144:
        for y in range(0,12): 
            i = []
            for x in range(0,12):
                num = y * 12 + x
                i.append(lst[num])
            rows.append(i)
        return rows
    
    elif len(lst) == 256:
        for y in range(0,16): 
            i = []
            for x in range(0,16):
                num = y * 16 + x
                i.append(lst[num])
            rows.append(i)
        return rows

def getSolution(dct):
    gridList = []
    newgrid = []
    gridList = DictToList(dct)
    newgrid = ListToGrid(gridList)
    newgrid = sg(newgrid)
    return newgrid


