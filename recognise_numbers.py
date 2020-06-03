#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:12:58 2020

@author: dewiballard
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import argparse
from pytesseract import image_to_string
import os


def get_string(x):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
        help="type of preprocessing to be done")
    args = vars(ap.parse_args())

    image = cv2.imread(args['puzzle_img.png'])
    print

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if args["preprocess"] == "thresh":
        y = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif args["preprocess"] == "blur":
            y = cv2.medianBlur(gray, 3)
            # write the grayscale image to disk as a temporary file so we can
            # apply OCR to it
            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print(text)
    # show the output images
    cv2.imshow("Image", image)
    cv2.imshow("Output", gray)
    cv2.waitKey(0)

print(get_string("puzzle_img.jpg"))