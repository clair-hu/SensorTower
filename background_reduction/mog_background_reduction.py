#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:00:47 2019

@author: clair
"""


"""
BackgroundSubtractorMOG
"""
import numpy as np
import cv2 as cv
cap = cv.VideoCapture('../KCF_tracker/videos/angle90.mp4')
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv.imshow('frame',fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()

"""
BackgroundSubtractorMOG2
"""
import numpy as np
import cv2 as cv
cap = cv.VideoCapture('../KCF_tracker/videos/angle90.mp4')
fgbg = cv.createBackgroundSubtractorMOG2()
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv.imshow('frame',fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()

"""
BackgroundSubtractorGMG
"""
import numpy as np
import cv2 as cv
cap = cv.VideoCapture('../KCF_tracker/videos/angle90.mp4')
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
fgbg = cv.bgsegm.createBackgroundSubtractorGMG()
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    cv.imshow('frame',fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()