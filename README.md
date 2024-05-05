# vision
This is a  vehile detection project using Computer Vision

Here I used background subtractions methods of OpenCV Library of Python and some morphological transformation for accuracy.
But this is for only static cameras. 

I have created an Android app to replicate the actual traffic light conditions and used firebase to push the vehicle detection numbers from OpenCV running on a raspberry Pi to Android app.

At the corner of the video frame you can see the count of the vehicles which gets recorded,when they cross a predefined limit,the count is pushed on firebase.

For the calculation of the object coordinates and object ids I defined a class called vehicles.py


