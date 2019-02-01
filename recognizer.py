"""
FACE RECOGNITION TO MQTT - main face recognition script

This uses the pi camera and compares detected faces from camera stream against stored user face data. 
If a match is detected it fires off an MQTT message with the name of the person detected
 
Usage:
1. Can either call it directly(python recognizer.py) or import it and call recognizeToMQTT()

"""

import face_recognition
import picamera
import numpy
import os
import pickle
import paho.mqtt.client as mqtt

#--- MQTT SETTINGS ---#
mqttHost = 'localhost' #required
mqttPort = 1883 #required
mqttUser = None #optional
mqttPassword = None #optional
mqttClientId = "face_recognition_to_mqtt" #each client needs a unique ID
mqttTopicPrefix = "cmnd/faceToMqtt/user/" #mqtt message will be this plus detected users name appended to end
mqttPayload = "detected"


def recognizeToMQTT():
    # Initialize Raspberry Pi camera.
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    newImg = numpy.empty((240, 320, 3), dtype=numpy.uint8)
    
    #mqtt initialization
    mqttClient = mqtt.Client(mqttClientId)
    #add password/username if set
    if mqttUser and not mqttPassword:
        mqttClient.username_pw_set(mqttUser)
    elif mqttUser and mqttPassword:
        mqttClient.username_pw_set(mqttUser, mqttPassword)      
    #connect to mqtt server
    mqttClient.connect(mqttHost, mqttPort)
    
    #variables for captured frame data
    faceLocations = []
    faceEncodings = []

    #retrieve stored vectors/encodings of user images
    data = pickle.loads(open(os.getcwd()+os.path.sep+"encodings.pickle", "rb").read())
        
    print("Beginning to watch for known faces...\n")
    while True:
        #capture a single frame/image
        camera.capture(newImg, format="rgb")

        #generate data for capture
        faceLocations = face_recognition.face_locations(newImg)    
        faceEncodings = face_recognition.face_encodings(newImg, faceLocations)

        #if a face is in the captured image loop over detected face data and compare to stored face data
        for faceEncoding in faceEncodings:
            #check for match
            match = face_recognition.compare_faces(data["encodings"], faceEncoding)
            matches=numpy.where(match)[0]
            #if a match then fire off mqtt message
            if len(matches)>0:
                name = str(data["names"][matches[0]])
                print("User detected {}!".format(name))
                mqttClient.publish( mqttTopicPrefix + name, mqttPayload )

    
if __name__ == "__main__":
	
    print("\n\n\nFACE RECOGNITION TO MQTT - main face recognition")     
    print("* captures frames from picamera and compares to see if a known user/person is captured")    
    print("* fires off an mqtt message if a known user/person is detected \n\n\n")    
    
    recognizeToMQTT()