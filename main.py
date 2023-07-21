import cv2
import os
import subprocess
import numpy as np
import winsound
import keyboard

# Set the source file path on the Raspberry Pi
source_file = '/home/katta/Desktop/qvideo1.h264'

rasp_ip = "192.168.121.206"
rasp_username = 'katta'

# Set the destination file path on the PC
destination_file = "D:\gtest"

# Set the PC's SSH address
pc_ssh_address = 'franticpc@192.168.121.220'

pscp_command = f'pscp.exe -P 22 {rasp_username}@{rasp_ip}:{source_file} {destination_file}'

# Execute the pscp command
subprocess.run(pscp_command, shell=True)

cap = cv2.VideoCapture("D:\gtest\qvideo1.h264")

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

currentFrame = 0
while(True):
      
    # reading from frame
    ret,frame = cap.read()
  
    if ret:
        # if video is still left continue creating images
        name = './data/img' + str(currentFrame) + '.jpg'
        print ('Creating...' + name)
  
        # writing the extracted images
        cv2.imwrite(name, frame)
  
        # increasing counter so that it will show how many frames are created
        currentFrame += 1
    else:
        break

# Load the pre-trained face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to detect eyes status in the given image
def detect_image(img):

    #Variable store execution state
    first_read = True

    #Converting the recorded image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Applying filter to remove impurities
    gray = cv2.bilateralFilter(gray,5,1,1)

    #Detecting the face for region of image to be fed to eye classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
    if(len(faces)>0):
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

            #roi_face is face which is input to eye classifier
            roi_face = gray[y:y+h,x:x+w]
            roi_face_clr = img[y:y+h,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_face,1.3,5,minSize=(50,50))
            
            #Examining the length of eyes object for eyes
            if(len(eyes)>=2):
                #Check if program is running for detection
                if(first_read):
                    return True
                else:
                    return True
            else:
                if(first_read):
                    return False
                else:
                    return False
            
    else:
        return False

# Folder containing the images
folder_path = 'D:\gtest\data'

# Counter for the number of images with open eyes
open_eyes_count = 0
closed_eyes_count = 0

# Iterate over the images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        # Perform eyes detection
    if 0 == detect_image(image):
        closed_eyes_count += 1
    else:
        open_eyes_count += 1

percentage = ((closed_eyes_count)/(closed_eyes_count+open_eyes_count))*100
print(f"PERCLOS: {percentage}")

if percentage > 65:
    stop_key = "ctrl+c"

    while True:
        duration = 2000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        # Check if the specified key is pressed
        if keyboard.is_pressed(stop_key):
            print("Stop key pressed. Exiting")
            break