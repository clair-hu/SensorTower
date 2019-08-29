#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 10:52:32 2019

@author: clair
"""

from imutils.video import VideoStream
import argparse
import imutils
import cv2
from random import randint
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())



trackers = {
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create
        }

#def isHittingBoundary(x, y, w, h, width, height):
#    
#    if x < 5 or y < 5 or (x+w) > 
        

def isInBboxes(x, y, w, h, bboxes):
    for a in range(x-3,x+4):
        for b in range(y-3, y+4):
            for w1 in range(w-3, w+4):
                for h1 in range(h-3, h+4):
                    if (a,b,w1,h1) in bboxes:
                        return True
    return False


bboxes = []
colors = []
multiTracker = cv2.MultiTracker_create()

vs = cv2.VideoCapture(args["video"])
firstFrame = None
startTime = time.time()
hasBounded = False

#video_width = vs.get(3)
#video_height = vs.get(4)


while True:
    frame = vs.read()
    
    frame = frame[1] if args.get("video", False) else frame
    
    if frame is None:
        break
    
    #resize frame
    frame = imutils.resize(frame, width=500)
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    gray = cv2.GaussianBlur(gray, (21, 21), 0)
#    
#    if firstFrame is None:
#        firstFrame = gray
#        continue
#
#    frameDelta = cv2.absdiff(firstFrame, gray)
#    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
#    
#    thresh = cv2.dilate(thresh, None, iterations=2)
#    # find contours on the thresholded image
#    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#    cnts = imutils.grab_contours(cnts)
    
    # loop over the contours
    currTime = time.time()
    deltaTime = currTime - startTime
    
    if hasBounded == False and deltaTime >= 0.2:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if firstFrame is None:
            firstFrame = gray
            continue
    
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        
        thresh = cv2.dilate(thresh, None, iterations=2)
        # find contours on the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        for c in cnts:
            
            if cv2.contourArea(c) < args["min_area"]:
                continue
            
            (x, y, w, h) = cv2.boundingRect(c)
#            if isInBboxes(x,y,w,h,bboxes):
#                continue
            bb = (x, y, w, h)
            print(bb)
            bboxes.append(bb)
            color = (randint(64, 255), randint(64, 255), randint(64, 255))
            colors.append(color)
            multiTracker.add(trackers[args["tracker"]](), frame, bb)
        if len(bboxes) >= 1:
            hasBounded = True
#            multiTracker.add(trackers[args["tracker"]](), frame, bb)
    
    
    (H, W) = frame.shape[:2]

    if bboxes != []:
        if len(bboxes) >= 1:
            (success, boxes) = multiTracker.update(frame)
            if success:
                print("AFTER SUCCESS")
                for i, box in enumerate(boxes):
                    (x, y, w, h) = [int(v) for v in box]
                    print(i, end=" ")
                    print((x, y, w, h))
                    cv2.rectangle(frame, (x,y), (x+w,y+h), colors[i], 2)
            else:
                print("FAILEDDDDDDDDDDDD")
                startTime = time.time()
                hasBounded = False
                bboxes = []
                colors = []
                multiTracker = cv2.MultiTracker_create()
                
                
                
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("s"):
        bb = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        print(bb)
        bboxes.append(bb)
        color = (randint(64, 255), randint(64, 255), randint(64, 255))
        colors.append(color)
        multiTracker.add(trackers[args["tracker"]](), frame, bb)
        
    elif key == ord("q"):
        break
    

    
    
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
    
cv2.destroyAllWindows()
cv2.waitKey(1)
            