"""
FACE RECOGNITION TO MQTT - dataset trainer script

This uses the pi camera to generate a set of sample images for a user, then computes and saves vector/encoding data for face detection comparisons later
 
Usage:
1. Can either call it directly(python trainer.py) or import it and call generateThenCompute()
2. All other instructions display while script is run

"""

import picamera
import os
import sys
import select
import time
import encoder

def generateThenCompute():
    #initialize picamera
    camera = picamera.PiCamera()

    while True:
        #Get persons name, used as directory name
        personName = input('What is the persons name we are generating data for? ')
        
        personDir = os.getcwd() + os.path.sep + "datastore" + os.path.sep + personName
        picCount = 1 #keep track of how many pictures taken
        if not os.path.isdir(personDir):
            try:
                os.makedirs(personDir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            print("Beginning to capture pictures every 2 seconds..")     
            print("When you are happy with the amount of samples type 'd' or 'done' and enter to begin encoding\n\n")      
            time.sleep(3)
            #enter loop until 'd'/'done' typed into cli or it is closed     
            while True:    
                while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                  #see if user is trying to close script
                  line = sys.stdin.readline()
                  if line.lower().strip()=="d" or line.lower().strip()=="done":         
                    print( "Done gathering data..." )       
                    camera.close()
                    encoder.computeEncodings()				
                    exit(1)
                  else: # an empty line means stdin has been closed     
                    camera.close()
                    exit(0)
                else:
                    camera.capture(personDir + os.path.sep + str(picCount) + ".jpg", format="rgb")                    
                    print( "Picture saved: " + str(picCount) + ".jpg" )   
                    picCount = picCount + 1
                    time.sleep(2)       
            
        else:
            ans = input("That person exists, add to existing persons dataset(y/n)")
            if(ans.lower() == 'y' or ans.lower() == 'yes'):
                print( "Beginning to capture pictures every 2 seconds..")        
                print( "When you are happy with the amount of samples type 'd' or 'done' and enter to begin encoding\n\n")  
                time.sleep(3) 
                existingData = os.listdir(personDir) 
                picCount = len(existingData) + 1  #set count to account for existing data
                #enter loop until 'd'/'done' typed into cli or it is closed      
                while True:
                    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                      #see if user is trying to close script
                      line = sys.stdin.readline()
                      if line.lower().strip()=="d" or line.lower().strip()=="done":         
                        print( "Done gathering data and exiting..." )       
                        camera.close()
                        encoder.computeEncodings()	
                        exit(1)
                      else: # an empty line means stdin has been closed     
                        camera.close()
                        exit(0)
                    else:
                        camera.capture(personDir + os.path.sep + str(picCount) + ".jpg", format="rgb")   
                        print("Picture saved: " + str(picCount) + ".jpg" )   
                        picCount = picCount + 1
                        time.sleep(2)
                

if __name__ == "__main__":
    
    print("\n\n\nFACE RECOGNITION TO MQTT - dataset generator script")     
    print("* no two people/users can have the same exact name")    
    print("* this script will take pictures every 2 seconds")     
    print("* if you wish to add data to an existing user just type existing users name below")     
    print("* type 'd' or 'done' and enter to stop taking pictures and begin encoding\n\n\n")    
    
    generateThenCompute()