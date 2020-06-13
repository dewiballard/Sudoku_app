#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:11:13 2020

@author: dewiballard
"""

import pytesseract
import cv2
import matplotlib.image as mpimg


n_cols = 9                                                  #these will be taken from global values already exist
n_cells = 250                                               #these will be taken from global values already exist
n_rows = int(n_cells/n_cols)


for i in range(n_rows):
    for j in range(n_cols):
        if len(str(i+1)) < 2:
            if len(str(j+1)) < 2:
                file_name = 'puzzle_img_' + '0' + str(i+1) + '_0' + str(j+1)
                print(file_name)
            else:
                file_name = 'puzzle_img_' + '0' + str(i+1) + str(j+1)
                print(file_name)
        else:
            if len(str(j+1)) < 2:
                file_name = 'puzzle_img_' + str(i+1) + '_0' + str(j+1)
                print(file_name)
            else:
                file_name = 'puzzle_img_' + str(i+1) + '0' + str(j+1)
                print(file_name)

img_cv = cv2.imread(r'puzzle_img.png')
img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
img_clean = cv2.GaussianBlur(img_gray, (5, 5), 0)

mpimg.imsave("out.png", img_clean, cmap="gray")             #delete unprocessed image when processed is saved
#os.remove()

global read
    
try:
    read = pytesseract.image_to_string(img_clean, config='--psm 10 -c tessedit_char_whitelist=0123456789', timeout=1) #only numbers recognised
except RuntimeError as timeout_error:
    pass

print(read)