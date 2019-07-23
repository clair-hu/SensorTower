#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:17:30 2019

@author: clair
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:29:27 2019

@author: clair
"""
from imutils.video import VideoStream
import argparse
import imutils
import cv2
from imutils.video import FPS
from random import randint

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

trackers = {
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create
        }

tracker = trackers[args["tracker"]]()

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
        if len(bboxes) == 1:
            (success, boxes) = tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in boxes]
                cv2.rectangle(frame, (x,y), (x+w,y+h), colors[0], 2)
        else:
            (success, boxes) = multiTracker.update(frame)
            if success:
                for i, box in enumerate(boxes):
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(frame, (x,y), (x+w,y+h), colors[i], 2)
       
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("s"):
        bb = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        bboxes.append(bb)
        color = (randint(64, 255), randint(64, 255), randint(64, 255))
        colors.append(color)
        multiTracker.add(cv2.TrackerKCF_create(), frame, bb)
        tracker.init(frame, bb)
        fps = FPS().start()
        
    elif key == ord("q"):
        break
    
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
    
cv2.destroyAllWindows()
cv2.waitKey(1)
            
            