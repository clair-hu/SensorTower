#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 18:02:54 2019

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

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

#trackers = {
#            "kcf": cv2.TrackerKCF_create,
#            "boosting": cv2.TrackerBoosting_create,
#            "mil": cv2.TrackerMIL_create
#        }
#
#tracker = trackers[args["tracker"]]()


# initialize bounding box
initBB = None

vs = cv2.VideoCapture(args["video"])

while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    
    if frame is None:
        break
    
<<<<<<< HEAD
#    #resize frame
#    frame = imutils.resize(frame, width=500)
#    (H, W) = frame.shape[:2]
=======
    #resize frame
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]
>>>>>>> 0f2ec6cdb188498a5df00f82cdbbe63f9ed533d7
#    
#    if initBB is not None:
#        (success, box) = tracker.update(frame)
#        
#        if success:
#            (x, y, w, h) = [int(v) for v in box]
#            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
#            
#        info = [("Success", "Yes" if success else "No")]
#        
#        for (i, (k,v)) in enumerate(info):
#            text = "{}: {}".format(k,v)
#            cv2.putText(frame, text, (10, H - ((i*20)+20)), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,255),2)
            
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
#    if key == ord("s"):
#        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
#        tracker.init(frame, initBB)
#        
#    elif key == ord("q"):
#        break
    
#if not args.get("video", False):
#    vs.stop()
#else:
#    vs.release()
    
cv2.destroyAllWindows()
<<<<<<< HEAD
cv2.waitKey(1)
=======
#cv2.waitKey(1)
>>>>>>> 0f2ec6cdb188498a5df00f82cdbbe63f9ed533d7
            
            