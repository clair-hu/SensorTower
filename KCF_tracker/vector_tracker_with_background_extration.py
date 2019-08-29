#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:36:16 2019

@author: clair
"""

import numpy as np
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
ap.add_argument("-a", "--min-area", type=int, default=100, 
    help="minimum area size")

args = vars(ap.parse_args())

vector_tracker = []

trackers = {
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create
        }

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


input_video = args["video"]
vs = cv2.VideoCapture(input_video)
_, frame = vs.read()
avg1 = np.float32(frame)
avg2 = np.float32(frame)
prev_frame = None
startTime = time.time()

hasBackgoundExtracted = False
while(True):
    if not hasBackgoundExtracted:
        _, frame = vs.read()
        
        if frame is None:
            print("frame none")
            if prev_frame is not None:
                print("prev_Frame not none")
                hasBackgoundExtracted = True
                output_pic = "output/background_" + (input_video.split("/")[-1]).split(".")[-2] + ".jpg"
                cv2.imwrite(output_pic, prev_frame)
                prev_frame = imutils.resize(prev_frame, width=500)
                background_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                background_frame = cv2.GaussianBlur(background_frame, (21, 21), 0)
                
                print("before sleep")
                time.sleep(1)
                print("after sleep")
                vs = cv2.VideoCapture(args["video"])
            continue
        
        print("before average")
        cv2.accumulateWeighted(frame,avg1,0.1)
        cv2.accumulateWeighted(frame,avg2,0.01)
         
        res1 = cv2.convertScaleAbs(avg1)
        res2 = cv2.convertScaleAbs(avg2)
     
        prev_frame = res2
        
#        cv2.imshow('img',frame)
#        cv2.imshow('avg1',res1)
        cv2.imshow('avg2',res2)
    #    key = cv2.waitKey(1) & 0xFF
    #    if key == ord("q"):
    #        break
    else:
    
        frame = vs.read()
        
        frame = frame[1] if args.get("video", False) else frame
        
        if frame is None:
            break
        
        #resize frame
        frame = imutils.resize(frame, width=500)
        
        # loop over the contours
        currTime = time.time()
        deltaTime = currTime - startTime
    
        if (len(bboxes) < 1 and deltaTime >= 0.1) or deltaTime > 5:
            
            # for comparison with gray and thresh frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            cv2.imshow("background_frame", prev_frame)
            frameDelta = cv2.absdiff(background_frame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            cv2.imshow("gray", gray)
            cv2.imshow("thresh", thresh)
            
            
            # find contours on the thresholded image
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            for c in cnts:
                
                if cv2.contourArea(c) < args["min_area"]:
                    continue
                
                (x, y, w, h) = cv2.boundingRect(c)
                if isInBboxes(x,y,w,h,bboxes):
                    continue
                
                bb = (x, y, w, h)
                print(bb)
                bboxes.append(bb)
                color = (randint(64, 255), randint(64, 255), randint(64, 255))
                colors.append(color)
                vector_tracker.append(trackers[args["tracker"]]())
                vector_tracker[-1].init(frame, bb)
                startTime = time.time()
        
        (H, W) = frame.shape[:2]
    
        if bboxes != []:
            if len(bboxes) >= 1:
                for i, bb in enumerate(bboxes):
                    (success, box) = vector_tracker[i].update(frame)
                    if success:
                        print(i)
                        print("success")
                        (x, y, w, h) = [int(v) for v in box]
                        cv2.rectangle(frame, (x,y), (x+w,y+h), colors[i], 2)
                    else:
                        print("FAILEDDDDDDDDDDDD")
                        vector_tracker.pop(i)
                        bboxes.pop(i)
                        colors.pop(i)
                        startTime = time.time()
                        
                    
                    
                    
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("s"):
            bb = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
            print(bb)
            bboxes.append(bb)
            color = (randint(64, 255), randint(64, 255), randint(64, 255))
            colors.append(color)
            vector_tracker.append(trackers[args["tracker"]]())
            vector_tracker[-1].init(frame,bb)
            
        elif key == ord("q"):
            break
    
    
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
    
cv2.destroyAllWindows()
cv2.waitKey(1)
            