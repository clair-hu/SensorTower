#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:00:47 2019

@author: clair
"""

import numpy as np
import cv2
import argparse

SUBTRACTOR = {
            "mog": cv2.bgsegm.createBackgroundSubtractorMOG,
            "mog2": cv2.createBackgroundSubtractorMOG2,
            "gmg": cv2.bgsegm.createBackgroundSubtractorGMG
        }

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-s", "--subtractor", type=str, help="background subtractor to apply on the video")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"])
background_subtractor = args["subtractor"]
# eg. '../KCF_tracker/videos/angle90.mp4'

fgbg = SUBTRACTOR[background_subtractor]()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

while(1):
    ret, frame = cap.read()
    
    if frame is None:
        break
    
    fgmask = fgbg.apply(frame)
    if background_subtractor == "gmg":
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('fgmask',frame)
    cv2.imshow('frame',fgmask)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

