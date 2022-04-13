import camera_module as camera_module
import numpy as np
import cv2

from tensorflow.keras.models import load_model


def pre_process(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img


def drive():
    motor.moveForward()
    while True:
        img = camera_module.takeImg()
        img = cv2.imread(img)
        img = np.asarray(img)
        img = pre_process(img)
        img = np.array([img])
        steering = float(model.predict(img))
        print(steering)
        motor.steer_to_prediction(steering)


if __name__ == "__main__":
    motor.calibrate()
    model = load_model('./model.h5')
    drive()
