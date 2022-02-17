import camera_module as camera_module
import numpy as np
import motor
from cv2 import imread, COLOR_RGB2YUV, cvtColor, GaussianBlur, resize
import os

from tensorflow.keras.models import load_model

if __name__ == "__main__":
    motor.calibrate()
    model = load_model(os.path.join(os.getcwd(), './model.h5'))


def pre_process(img):
    img = img[54:120, :, :]
    img = cvtColor(img, COLOR_RGB2YUV)
    img = GaussianBlur(img,  (3, 3), 0)
    img = resize(img, (200, 66))
    img = img/255
    return img


def drive():
    motor.moveForward()
    while True:
        img_path = camera_module.takeImg()
        img = imread(img_path)
        img = np.asArray(img)
        img = pre_process(img)
        steering = float(model.predcit(img))
        motor.steer_to_prediction(steering)
