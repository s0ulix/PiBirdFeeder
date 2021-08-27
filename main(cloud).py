
#importing modules
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime
import json
import base64
import requests


#function for calling the api which returns the name of the bird
def call_api(img_name):

    #creating base64 of the image with proper format and encoding
    with open(img_name, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        my_string = my_string.decode('utf-8')
        my_string = ',' + my_string

    #creating a dictionary which will later become json
    b = {"image": my_string}

    #headers to pass in the api call
    Headers = {'Content-type': 'application/json'}

    #creating json data from the dictionary to pass in the body of the api call
    jsonData = json.dumps(b)

    url="Enter your api url here"
    
    #calling the api and getting the response as response
    response = requests.post(url, headers=Headers, data=jsonData)

    #returning the reponse
    return response

#function to capture the image from the camera
def cap_img():

    #opening camera object
    with picamera.PiCamera() as camera:

        #configuring resolution of the camera
        camera.resolution = (1024, 768)

        #loop for taking n pitures chnge the range value to your preferred number of images when motion detected
        for i in range(3):

            #getting present time
            now = datetime.now()

            #creating a file name as per the present time
            img_name = "/home/pi/Desktop/cv/Pi_Image_{}.png".format(now)

            #capturing the image and saving it by the name of the file name created above
            camera.capture(img_name)

            #printing that the image is captured
            print("{} written!".format(img_name))

            #calling the api to get the name of the bird
            res=call_api(img_name)

            #opening result txt file to add the result into the result.txt
            with open("/home/pi/Desktop/cv/result.txt","a+") as txt_file:

                #writing result with the name of the image
                txt_file.write(img_name+" - "+res.content+"\n")

            #printing result
            print(img_name+"-"+res.content)

#GPIO configurations
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#pin number where the motion detector is attached
#Note: its the physical pin no not the gpio number
pin_no=40

#stting the pin for the input from motion detector
GPIO.setup(pin_no, GPIO.IN)

#while true loop to work untill the program is not stopped 
while True:

    #getting output of the motion detector in variable i, 1 for motion and 0 for no motion
    i=GPIO.input(pin_no)

    #if motion is detected execute if block
    if i==1:

        #printing the motion detected
        print( "Motion detected")

        #calling the function to capture the image which will futhur call the api function
        cap_img()

        #waiting for one second
        time.sleep(1)
    else:
        
        #waiting for 1 second
        time.sleep(1)
