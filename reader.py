# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:49:24 2020

@author: pm11lms
"""


import cv2
import numpy as np
import time 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\pm11lms\AppData\Local\Tesseract-OCR\tesseract.exe"

start = time.clock()
im = cv2.resize(cv2.imread('puzzle_img.png'), (1080, 1080))
out = np.zeros((9, 9), dtype=np.uint8)

for x in range(9):
    for y in range(9):
        num = pytesseract.image_to_string(im[10 + x*120:(x+1)*120 - 10, 10 + y*120:(y+1)*120 - 10, :], lang ='eng', config='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789')
        if num:
            out[x, y] = num
            
end = time.clock() - start
print("Time taken to solve: " + str(end))