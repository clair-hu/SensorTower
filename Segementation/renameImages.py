#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:14:30 2019

@author: clair
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

raw_image_path = "./raw_image"
renamed_image_path = "./renamed_image"

def loadImages(path):
    '''Put files into lists and return them as one list with all images 
     in the folder'''
    image_files = sorted([os.path.join(path, file)
                          for file in os.listdir(path)
                          if file.endswith('.png') or file.endswith('.jpg') or file.endswith('jpeg')])
    return image_files

"""# **Displaying Images**"""

# Display two images
def display(a, b, title1 = "Original", title2 = "Edited"):
    plt.subplot(121), plt.imshow(a), plt.title(title1)
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(b), plt.title(title2)
    plt.xticks([]), plt.yticks([])
    plt.show()

# Display one image
def display_one(a, title1 = "Original"):
    plt.imshow(a), plt.title(title1)
    plt.show()


def make_dir(path):
    try:
        os.makedirs(path)
    except:
        pass

# Preprocessing
def processing(data, subdir):
    # Reading all images to work
    img = [cv2.imread(i, cv2.IMREAD_UNCHANGED) for i in data]
    try:
        print('Original size',img[0].shape)
    except AttributeError:
        print("shape not found")
   
    c = 0
    
    print(os.path.join(renamed_image_path, subdir))
    make_dir(os.path.join(renamed_image_path, subdir))
    
    for i in img:
        newimg_name = os.path.join(renamed_image_path, subdir, "timbertruck" + str(c) + ".jpg")

        c += 1
        cv2.imwrite(newimg_name, i)

    


"""# Main Function the heart of the program"""

def main():
    # calling global variable
    global image_path
    '''The var Dataset is a list with all images in the folder '''
    for i in os.listdir(raw_image_path):
        image_path = os.path.join(raw_image_path, i)
        
        try:
            dataset = loadImages(image_path)
        except:
            print("error message")
        
        print("List of files the first 3 in the folder:\n",dataset[:3])
        print("--------------------------------")
        
        # sending all the images to pre-processing
        processing(dataset, i)
   

  
main()