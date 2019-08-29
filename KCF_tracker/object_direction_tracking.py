#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 17:19:42 2019

@author: clair
"""


from imutils.video import VideoStream
import argparse
import imutils
import cv2
from random import randint
import time
from collections import deque
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
    help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
    help="OpenCV object tracker type")
ap.add_argument("-s", "--subtractor", type=str, default="mog",
    help="background subtractor to apply on the video")
ap.add_argument("-a", "--min-area", type=int, default=300, 
    help="minimum area size")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")

args = vars(ap.parse_args())


# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
chosen_object = None

vector_tracker = []

trackers = {
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create
        }
        
SUBTRACTOR = {
            "mog": cv2.bgsegm.createBackgroundSubtractorMOG,
            "mog2": cv2.createBackgroundSubtractorMOG2,
            "gmg": cv2.bgsegm.createBackgroundSubtractorGMG
        }

background_subtractor = args["subtractor"]
fgbg = SUBTRACTOR[background_subtractor]()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

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

vs = cv2.VideoCapture(args["video"])
firstFrame = None
startTime = time.time()

while True:
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

        fgmask = fgbg.apply(frame)

        if firstFrame is None:
            firstFrame = fgmask
            continue

        fgmaskthresh = cv2.dilate(fgmask, None, iterations=2)
        if background_subtractor == "gmg":
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            fgmaskthresh = fgmask

#        cv2.imshow("fgmask", fgmaskthresh)
        
        
        # find contours on the thresholded image
        cnts = cv2.findContours(fgmaskthresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        index = -1
        
        for i, c in enumerate(cnts):
            
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
#            if max_contour == c:
#                index = i
#                print("found max countour!")
#                ((x, y), radius) = cv2.minEnclosingCircle(c)
#                M = cv2.moments(c)
#                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#                chosen_object = bb
#                colors[-1] = (14, 0, 0)
#                pts.appendleft(center)
                
            vector_tracker.append(trackers[args["tracker"]]())
            vector_tracker[-1].init(frame, bb)
            startTime = time.time()
            
#        '''
#        for direction
#        '''
#        if len(colors) >= 3:
#            c = cnts[index]
#            ((x, y), radius) = cv2.minEnclosingCircle(c)
#            M = cv2.moments(c)
#            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#            chosen_object = bb
#            colors[2] = (14, 0, 0)
#            pts.appendleft(center)
    
    (H, W) = frame.shape[:2]

#    if bboxes != []:
    if len(bboxes) >= 1:
        for i, bb in enumerate(bboxes):
            (success, box) = vector_tracker[i].update(frame)
            if success:
                print("success")
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x,y), (x+w,y+h), colors[i], 2)
            else:
                print("FAILEDDDDDDDDDDDD")
                vector_tracker.pop(i)
                bboxes.pop(i)
                colors.pop(i)
                startTime = time.time()
#                    firstFrame = None
         
            
    if len(cnts) > 5:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
        if radius > 35:
            pts.appendleft(center)
    '''
    tracking center of the chosen object
    '''
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 10 and i == 1 and len(pts) >= 10 and pts[-10] is not None:
#        if counter >= 10 and i == 1:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")

            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the movement deltas and the direction of movement on
    # the frame
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)
                    
                
                
                
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    
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
    
#time.sleep(10)
#cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
            