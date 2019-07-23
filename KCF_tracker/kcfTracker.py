#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:10:58 2019

@author: clair
"""

import cv2
import sys
from random import randint
import argparse

#trackerType = "KCF"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
#ap.add_argument("-o", "--output", required=True,
#	help="path to output video")
ap.add_argument("-t", "--tracker", default="KCF",
                help="object tracker algorithm to apply on the input video")
#ap.add_argument("-t", "--threshold", type=float, default=0.3,
#	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

trackerType = args["tracker"]
videoPath = args["input"]

# Create a video capture object to read videos
videoCapture = cv2.VideoCapture(videoPath)

# Read first frame
success, frame = videoCapture.read()

# quit if unable to read the video file
if not success:
  print('Failed to read video')
  sys.exit(1)

## Select boxes
bboxes = []
colors = []

# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
while True:
  # draw bounding boxes over objects
  # selectROI's default behaviour is to draw box starting from the center
  # when fromCenter is set to false, you can draw box starting from top left corner
  bbox = cv2.selectROI('MultiTracker', frame)
  bboxes.append(bbox)
  colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
  print("Press q to quit selecting boxes and start tracking")
  print("Press any other key to select next object")
  k = cv2.waitKey(0) & 0xFF
  if (k == 113):  # q is pressed
    break

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker 
for bbox in bboxes:
#    multiTracker.add(createTrackerByName(trackerType), frame, bbox)
  multiTracker.add(cv2.TrackerKCF_create(), frame, bbox)
  
# Process video and track objects
while videoCapture.isOpened():
  success, frame = videoCapture.read()
  if not success:
    break

  success, boxes = multiTracker.update(frame)
  # draw tracked objects
  for i, newbox in enumerate(boxes):
    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    
# show frame
  cv2.imshow('MultiTracker', frame)
  

  # quit on ESC button
  if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
    break
