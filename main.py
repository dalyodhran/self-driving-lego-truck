import camera_module as camera_module
import numpy as np
import motor
import cv2
import os
from buildhat import Motor

from tensorflow.keras.models import load_model

# Steering sentivity can be adjusted, it's 1 but default
steeringSen = 1
model = load_model(os.path.join(os.getcwd(), '/model.h5'))
motor_lr = Motor('A')

def preProcess(img):
    img = img[54:120,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img

motor.moveForward()

while True
    imgPath = camera_module.takeImg()
    img = cv2.imread(imgPath)
    img = np.asArray(img)
    img = preProcess(img)
    img = array([img])
    steering = float(model.predcit(img))
    print("Predicted Steering value: " + steering)
    steering = steering * steeringSen
    print("Steering value after sensitivity applied: " + steering)

    # using this directly from build hat because in the motor.py there's only turn right and turn left
    # but the value we get from the model should automatically be positive or negative
    motor_lr.run_for_degrees(steering)
