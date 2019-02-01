# Face Recognition to MQTT

This is not meant to be the only method of presence detection. It is built for and tested on a piZero with picamera but should work with any pi. Its simple in function, if a face it recognizes crosses through its view it fires off an mqtt message saying it detected the person by name. Then you handle the rest in your prefered home automation setup.

For anyone who has messed with presence detection methods in homebrew home automation setups most options are not always accurate/fast enough. Layering the various detection methods improves things greatly. This is just meant to be another layer in that stack.


### Usage:
It consists of 3 files.
  - trainer.py - run this file and it will take pictures every 2 seconds(using the pi camera) to gather data for a user. And then encode that data for use in facial recognition
  - encoder.py - if you have your own set of images(must be jpg) for a person place the images in their own directory within the datastore directory. Name the directory after the person they represent(eg.. /datastore/fred/1.jpg). After that run this script and it will generate the vectors/encodings for the images for use later in facial recognition
  - recognizer.py - this is the main facial recogntion script. It will capture frames from the pi camera stream, check to see if it recognizes any faces in the frame and then fire off an mqtt message if it detects a known person(edit this file with your mqtt credentials) 
  
### Dependencies:
* [dlib](http://dlib.net/) - deep learning library
* [face_recognition](https://github.com/ageitgey/face_recognition) - python face recognition library
* [paho-mqtt](https://pypi.org/project/paho-mqtt/) - MQTT module for python
* [picamera](https://picamera.readthedocs.io/en/release-1.13/) - picamera module for python
* [numpy](http://www.numpy.org/) - numpy python library


