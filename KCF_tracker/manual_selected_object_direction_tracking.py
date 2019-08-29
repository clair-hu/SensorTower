#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 17:43:25 2019

@author: clair
"""

from imutils.video import VideoStream
import argparse
import imutils
import cv2
from imutils.video import FPS
from random import randint
from collections import deque
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())



trackers = {
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create
        }

#tracker = trackers[args["tracker"]]()


# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""


fps = None

bboxes = []
colors = []
multiTracker = cv2.MultiTracker_create()

vs = cv2.VideoCapture(args["video"])

while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    
    if frame is None:
        break
    
    #resize frame
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    if bboxes != []:
        if len(bboxes) >= 1:
#            (success, boxes) = tracker.update(frame)
#            if success:
#                (x, y, w, h) = [int(v) for v in boxes]
#                cv2.rectangle(frame, (x,y), (x+w,y+h), colors[0], 2)
#        else:
            (success, boxes) = multiTracker.update(frame)
            if success:
                for i, box in enumerate(boxes):
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(frame, (x,y), (x+w,y+h), colors[i], 2)
                    
                    print("update")
                    print(len(bboxes))
                    center = ((int)(box[0]+box[2]/2)), ((int)(box[1]+box[3]/2))
                    print(center)
                    pts.appendleft(center)
                    
    
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    
    if key == ord("s"):
        pts.clear()
        bb = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        print(bb)
        bboxes.append(bb)
        color = (randint(64, 255), randint(64, 255), randint(64, 255))
        colors.append(color)
       
        multiTracker.add(trackers[args["tracker"]](), frame, bb)
#        tracker.init(frame, bb)
        fps = FPS().start()
        
    elif key == ord("q"):
        break
    
#    if len(bboxes) >= 1:
#        center = ((int)(bb[0]+bb[2]/2)), ((int)(bb[1]+bb[3]/2))
#        print(center)
#        pts.appendleft(center)

    
    '''
    tracking center of the chosen object
    '''
    print(len(pts))
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 5 and i == 1 and len(pts) >= 10 and pts[-10] is not None:
#        if counter >= 10 and i == 1:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")

            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 3:
                dirX = "East" if np.sign(dX) == 1 else "West"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 3:
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
    print(direction)
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)
        
    cv2.imshow("Frame", frame)
                    
    
    
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
    
cv2.destroyAllWindows()
cv2.waitKey(1)
            
            