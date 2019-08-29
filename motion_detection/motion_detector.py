#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:04:41 2019

@author: clair
"""

"""
background subtraction
use cases:
    count number of cars passing through a toll booth
    count number of people walking in and out of a store
    motion detection
    
"The background of our video stream is largely static and unchanging over consecutive frames of a video. 
Therefore, if we can model the background, we monitor it for substantial changes. 
If there is a substantial change, we can detect it
— this change normally corresponds to motion on our video."

"Now obviously in the real-world this assumption can easily fail. Due to shadowing, reflections, lighting conditions, and any other possible change in the environment, our background can look quite different in various frames of a video. And if the background appears to be different, it can throw our algorithms off. That’s why the most successful background subtraction/foreground detection systems utilize fixed mounted cameras and in controlled lighting conditions."

"""

#from imutils.video import VideoStream
import imutils
from imutils.video import VideoStream
import argparse
import datetime
import time
import cv2

# construct the argument parse and parse the command line arguments
ap = argparse.ArgumentParser()

# video optional
ap.add_argument("-v", "--video", help="path to the video file")


ap.add_argument("-a", "--min-area", type=int, default=300, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if not args.get("video", None):
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args["video"])
    
# initialize the first frame in the video stream
firstFrame = None
while True:
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
    if frame is None:
        break
    
    # the performance of the object detection is related with the frame size set by the opencv model.
    # Decreasing frame size is saving the computation, thus having better performance in better detecting speed.
    # after tuning parameters, 300 seems to have the best performance
<<<<<<< HEAD
    frame = imutils.resize(frame, width=500)
=======
    frame = imutils.resize(frame, width=300)
>>>>>>> 0f2ec6cdb188498a5df00f82cdbbe63f9ed533d7
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
    
    # loop over the contours
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        
        (x, y, w, h) = cv2.boundingRect(c)
<<<<<<< HEAD
        a = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
=======
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
>>>>>>> 0f2ec6cdb188498a5df00f82cdbbe63f9ed533d7
        text = "Occupied"
        
    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%P"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
    
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
    