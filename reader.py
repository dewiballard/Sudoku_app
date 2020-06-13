# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 20:52:28 2020

@author: dewiballard
"""

import cv2
import numpy as np
import pytesseract

img = cv2.imread('puzzle_img.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_clean = cv2.GaussianBlur(img_gray, (5, 5), 0)
img_resize = cv2.resize(img_clean, (1080, 1080))
ret, thresh = cv2.threshold(img_resize, 5, 255, cv2.THRESH_OTSU)
cv2.imwrite("./output_image.png", thresh)
n_cols=9
slicer = int(1080/n_cols)
margin = 10
out = np.zeros((n_cols, n_cols), dtype=np.uint8)
for x in range(9):
    for y in range(9):
        num = pytesseract.image_to_string(thresh[margin + x*slicer:(x+1)*slicer - margin, margin + y*slicer:(y+1)*slicer - margin], lang ='eng', config='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789')
        if num:
            out[x, y] = num
print(out)