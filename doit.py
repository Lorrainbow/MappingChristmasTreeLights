#!/usr/bin/env python3
from picamera.array import PiRGBArray
from picamera import PiCamera
from xmlrpc.client import ServerProxy
import cv2
import numpy as np
import imutils
import time

class Camera:
    RESOLUTION = (640,480)
    camera = PiCamera(framerate=6) #make camera class level
    camera.hflip = True
    camera.vflip = True
    camera.resolution = RESOLUTION
    camera.iso = 800

    def __init__(self, iso=800):
        self.iso = iso
        self.rawCapture = PiRGBArray(self.camera)
        self.camera.iso=self.iso

    def set_exposure(self, shutter_speed, awb_gains):
        """Set exposure for the camera - ensures consistent images"""
        self.camera.exposure_mode = 'off'
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = awb_gains
        self.camera.shutter_speed = shutter_speed
        
        
    def get_exposure(self):
        """Get current exposure settings for this camera"""
        self.camera.iso = self.iso
        self.camera.exposure_mode = "auto"
        self.camera.awb_mode = "auto"
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now return the values
        return (self.camera.exposure_speed, self.camera.awb_gains)

    def get_image(self):
        """get an image from the camera, in format suitable for use with OpenCV"""
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array
        return image

def find_light(base, image):
    """Get coordinates for the light"""
    # convert images to use int16 data types
    # this is a signed data type so we don't get overflow on subtraction
    # we also isolate the red channel only
    base = np.array(base[:,:,0], dtype="int16")
    image = np.array(image[:,:,0], dtype="int16")
    
    #subtract the base image; the only part that has changed is the neopixel
    result = image - base
    
    #identify the parts of the image that have a large change in brightness
    result = cv2.inRange(result, 100, 255)
    
    #remove small areas
    mask = cv2.erode(result, None, iterations=1)
    mask = cv2.dilate(result, None, iterations=1)
    
    #find the contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        #get the biggest contour
        c = max(cnts, key=cv2.contourArea)
        
        #and find the center of it
       	M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"]) 
        return cX, cY
    #no neopixel found, so return -1, -1 to show this
    return -1, -1

cam  = Camera()

#connect to the RasPi connected to the tree
proxy = ServerProxy("http://stairlights.local:8000", allow_none = True)

#turn all the lights off
proxy.clear()

#make the images consistent
time.sleep(2)
settings = cam.get_exposure()
cam.set_exposure(*settings)
time.sleep(1)

#get our image with no lights on
base = cam.get_image()
for i in range(100):
    proxy.light_one(i)
    image = cam.get_image()
    points = find_light(base, image)
    print(i, points)
proxy.clear()
