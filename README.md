# Sensor Tower Mac Version

Developed via python script, running on mac, either with webcam, or with videos.


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



# Outlines
-   Sensor tower

    -   Mac version

        -   AI Based algorithm

            -   creating new virtual environment for opencv and yolo

                -   using pre-trained yolov3 model

                    -   two use cases

                        -   on webcam

                        -   on video

                -   <https://github.com/clair-hu/SensorTower/tree/master/yolo_object_detection>

        -   non AI based algorithm

            -   After tuning parameters, I found that the performance of
                the object detection is related with the frame size set
                by opencv.

                -   the speed of the python script is related with frame
                    size

                    -   need to decrease frame size to ensure the speed

            -   Background cleaning

                -   two methods

                    -   background subtractor by openCV

                        -   MOG

                            -   pros

                                -   works good on mac

                                -   performance better on android
                                    application

                        -   MOG2

                            -   pros

                                -   invariant to lighting change

                            -   cons

                                -   too much noise in practise

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

                                -   success

            -   Apply multiple type of trackers

                -   KCF

                    -   fastest

                -   Boosting

                -   MIL

            -   Get direction of moving object

                -   kcf tracker does not provide direction vector

                -   get directions from movement of the center of the
                    bounding boxes

        -   implemented in python

            -   code in github

                -   write README in github

                    -   connect the sequence of mindmap and codebase in
                        github


### Note
Due to git size limitation, raw images and resized images are back up in google drive.

More details in Mindmap https://app.mindmup.com/map/_free/2019/08/2a268320cb5011e981329f667c339e20
