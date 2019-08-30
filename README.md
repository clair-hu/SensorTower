# SensorTower


## Non AI based algorithm

### Flow

1. Background cleaning

2. auto object initialization

3. Apply KCF object tracker to moving object

4. Apply multiple kcf trackers

5. Apply multiple type of trackers

6. Get direction of moving object

## AI based algorithm

### Flow

1. creating new virtual environment for opencv and yolo

2. using pre-trained yolov3 model

3. train customized yolo model with pre-trained yolotiny model

-   sensor tower


## Three implementations

        -   on mac

            -   AI Based algorithm

                -   creating new virtual environment for opencv and yolo

                    -   using pre-trained yolov3 model

                        -   two use cases

                            -   on webcam

                            -   on video

                    -   <https://github.com/clair-hu/SensorTower/tree/master/yolo_object_detection>

            -   non AI based algorithm

                -   After tuning parameters, I found that the
                    performance of the object detection is related with
                    the frame size set by opencv.

                    -   the speed of the python script is related with
                        frame size

                        -   need to decrease frame size to ensure the
                            speed

                -   Background cleaning

                    -   two methods

                        -   background subtractor by openCV

                            -   MOG

                                -   pros

                                    works good on mac

                                    performance better on android
                                    application

                            -   MOG2

                                -   pros

                                    invariant to lighting change

                                -   cons

                                    too much noise in practise

                            -   GMG

                                -   with most noice

                            -   <https://docs.opencv.org/3.4.1/db/d5c/tutorial_py_bg_subtraction.html>

                        -   running average

                            -   over a number of frames

                            -   algorithm developed by clair

                -   auto object initialization

                    -   get clean background

                        -   subtract the current frame from the clean
                            background

                            -   <https://trello.com/c/rmqwQlVj/449-auto-object-tracker-without-human-select-bounding-box>

                -   Apply KCF object tracker to moving object

                -   Apply multiple kcf trackers

                    -   two methods

                        -   using multiTracker class by openCV

                            -   only has one response for whole trackers

                        -   customized vector of trackers

                            -   have response (success/failure) for each
                                trackers

                                -   easy for tracker management

                                    success

                -   Apply multiple type of trackers

                    -   KCF

                        -   fastest

                    -   Boosting

                    -   MIL

                -   Get direction of moving object

                    -   kcf tracker does not provide direction vector

                    -   get directions from movement of the center of
                        the bounding boxes

            -   implemented in python

                -   code in github

                    -   write README in github

                        -   connect the sequence of mindmap and codebase
                            in github

        -   on android platform

            -   implemented by java opencv

                -   github

                    -   add README

            -   building opencv-android library

                -   it is no longer maintained by opencv

                    -   last maintenance in August, 2018

                        -   <https://sourceforge.net/projects/opencvlibrary/files/opencv-android/>

                -   found workaround to build opencv-android library

                    -   using opencv build python script

                        -   <https://answers.opencv.org/question/197296/android-object-tracking/>

            -   connect android application with opencv-android library
                as a module

                -   <https://heartbeat.fritz.ai/a-guide-to-preparing-opencv-for-android-4e9532677809>

                -   <https://android.jlelse.eu/a-beginners-guide-to-setting-up-opencv-android-library-on-android-studio-19794e220f3c>

            -   based on the development flow on Mac platform

                -   "translate" python opencv to android java opencv

                    -   using MOG background subtractor

                    -   using KCF tracker

            -   orientation of frame is wrong

                -   fix by doing matrix calculation

                    -   describe in codes

            -   defined min and max area for bounding boxes

                -   for performance

                    -   if the camera close to the cars, need to adjust
                        min of bounding box, increase the min area

            -   issue

                -   the speed of the application is still not quick
                    enough

                    -   usually it has 1 to 3 seconds delay

                        -   i think the issue is that the phone camera
                            can only process around 10 frame per minute,
                            but the algorithm wants to process around 25
                            to 30 frame per second.

                            -   described as the synchronization issue
                                between kcf and camera

                -   todo

                    -   sync phone camera capture speed with the speed
                        of kcf tracker algorithm

                        -   solution by Melvin

                            -   on android

                        -   clair no time to look at the synchronization
                            solution

        -   on jetson nano board

            -   openDataCam

                -   setup

                    -   instructions

                        -   <https://github.com/opendatacam/opendatacam/blob/master/documentation/jetson/JETSON_NANO.md>

                    -   buy all equipments for the project

                        -   thanks to shahril and clair

                    -   set up the new SD card

                        -   Write Image to the microSD Card

                            -   Note: the mac SD card adapter port is
                                not working

                                -   has to format and write image on the
                                    windows machine

                            -   need to download "Jetson Nano Developer
                                Kit SD Card Image" first

                                -   usually takes 1 hour

                        -   Setup and First Boot

                    -   verify if CUDA is in your PATH

                    -   set up 10w power instead of 5w power

                        -   put jumper on the J48 pin

                        -   5w not sufficient for the monitor display

                    -   set up a swap partition

                        -   setup a 6GB swap partition. (Nano has only
                            4GB of RAM)

                    -   set up wifi dongle

                        -   NOTE: have to do this before set up
                            opendatacam

                            -   this step has sudo apt update & upgrade

                                -   will ruin the dependency of
                                    opendatacam

                                    so have to do wifi dongle setup
                                    before opendatacam installation

                        -   note on the two dongles

                            -   small one does not work

                    -   verify USB camera

                        -   NOTE

                            -   two additional cameras

                                -   raspberry pi camera v2

                    -   install Opendatacam

                    -   setup a wifi connection in jetson nano board

                        -   as hotspot

                            -   currently has one named "jetson"

                                -   <https://github.com/opendatacam/opendatacam/blob/master/documentation/WIFI_HOTSPOT_SETUP.md>

                            -   password

                                -   kai

                                -   in the innovation password evernote

                -   export detected object to images

                    -   two tried methods but not working so far

                        -   cannot crop the original frame with the
                            bounding box properties (x,y,width,height)

                            -   can crop the original frame and the
                                bounding box frame

                        -   tried two APIs to crop visible webpage
                            content by Javascript

                            -   instead of cropping canvas

                                -   two APIs

                                    Croppie

                                    html2canvas

                                -   approach was to crop the display on
                                    the monitor

                -   train customized yolo model

                    -   for timbertruck model

                        -   timbertruck dataset

                            -   scraped from internet and label by
                                python script

                        -   training model

                            -   two instructions

                                -   using OpenImagesV4

                                    <https://www.learnopencv.com/training-yolov3-deep-learning-based-custom-object-detector/>

                                -   using self labeled images

                                    \[https://medium.com/\@manivannan\_data/how-to-train-yolov3-to-detect-custom-objects-ccbcafeb13d2\](https://medium.com/\@manivannan\_data/how-to-train-yolov3-to-detect-custom-objects-ccbcafeb13d2)

    -   prepare images

        -   some good resources

            -   vehicle data

                -   <http://www.gti.ssr.upm.es/data/Vehicle_database.html>

            -   <https://chatbotslife.com/vehicle-detection-and-tracking-using-computer-vision-baea4df65906>

            -   <https://medium.com/implodinggradients/self-driving-car-engineer-nanodegree-is-it-worth-it-8c675735cbd4>

            -   <https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/>

            -   datasets

                -   [1.](http://www.cvpapers.com/datasets.html)

                -   [2.](http://www.image-net.org/)

                -   [3.](http://pascallin.ecs.soton.ac.uk/challenges/VOC/)

        -   scraped  timber truck images from google images

            -   instead of using Udacity

                -   due to bad quality

            -   malaysia

                -   china

                    -   usa

                        -   canada

            -   using API Google Images Download

                -   <https://github.com/hardikvasa/google-images-download>

        -   manually clean bad images

        -   rename images

        -   resize images

            -   optional

                -   included in the step of training customized yolo
                    model

    -   image preprocessing

        -   <https://towardsdatascience.com/image-pre-processing-c1aec0be3edf>

        -   Checked Trifacta and dataspark, they do not provide image
            labeling, only structured data wrangling for csv, json...

    -   image labeling

        -   using labeling python script

            -   YOLO-Annotation-Tool-New

                -   <https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool>

    -   dataset preparation

        -   \[https://medium.com/\@manivannan\_data/how-to-train-yolov2-to-detect-custom-objects-9010df784f36\](https://medium.com/\@manivannan\_data/how-to-train-yolov2-to-detect-custom-objects-9010df784f36)


### Note
Due to git size limitation, raw images and resized images are back up in google drive.

More details in Mindmap https://app.mindmup.com/map/_free/2019/08/2a268320cb5011e981329f667c339e20
