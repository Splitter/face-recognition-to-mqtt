"""
FACE RECOGNITION TO MQTT - dataset encoder script

This is the encoder. It traverses the datastore importing and generating vectors/encodings for each jpeg image in the datastore
 
Usage:
1. Can either call it directly(python encoder.py) or import it and call computeEncodings()

"""

import os
import face_recognition
import pickle

def computeEncodings():
    print("Begin computing vectors...")
    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []
    # get root directory
    rootDir = os.getcwd()

    for subDir, dirs, files in os.walk(rootDir+os.path.sep+"datastore"):
        for file in files:
            if not file.endswith(".jpg"):
                continue
                
            filepath = subDir + os.sep + file
            name =  subDir.split(os.path.sep)[-1]
            print("Computing for user: "+name)
            #compute vectors
            print("Generating from file: "+file)
            image = face_recognition.load_image_file(filepath)
            face_locations = face_recognition.face_locations(image,model='hog')
            encodings = face_recognition.face_encodings(image, face_locations)
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
                
            print("Done with file: "+file)
    print("\n\nSaving encodings to : ")
    print(rootDir+os.path.sep+"encodings.pickle")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(rootDir+os.path.sep+"encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()
    print("Finished!")           



if __name__ == "__main__":
	
    print("\n\n\nFACE RECOGNITION TO MQTT - dataset encoder script")     
    print("* traverses datastore directory and computes vectors for all user images\n\n\n")    
    
    computeEncodings()