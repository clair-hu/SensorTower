#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:36:16 2019

@author: clair
"""

import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
ap.add_argument("-a", "--min-area", type=int, default=300, 
    help="minimum area size")

args = vars(ap.parse_args())
 
c = cv2.VideoCapture(args["video"])
_,f = c.read()
 
avg1 = np.float32(f)
avg2 = np.float32(f)
prev_frame = None

while(1):
    _,f = c.read()
    
    if f is None:
        break
     
    cv2.accumulateWeighted(f,avg1,0.1)
    cv2.accumulateWeighted(f,avg2,0.01)
     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)
 
    prev_frame = res2
    
    cv2.imshow('img',f)
    cv2.imshow('avg1',res1)
    cv2.imshow('avg2',res2)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

#cv2.imshow('prev_frame',prev_frame)
cv2.imwrite("prev_frame.jpg" , prev_frame)
c.release() 
cv2.destroyAllWindows()
cv2.waitKey(1)