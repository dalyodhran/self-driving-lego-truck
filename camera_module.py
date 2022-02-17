from picamera import PiCamera
from datetime import datetime
from pathlib import Path
import os


def takeImg(savePath=str(Path().absolute()) + "/"):

    timeNow = datetime.now().strftime("%H_%M_%S")
    imageFileName = "image_" + timeNow + ".jpg"
    image_path = os.path.join(savePath, imageFileName)
    camera.capture(image_path, resize=(480, 240))

    return image_path


def warmUpCamera():
    camera.start_preview()
    camera.resolution = (852, 480)


def shutDownCamera():
    camera.stop_preview()


if __name__ == '__main__':
    counter = 0
    while (counter < 10):
        takeImg()
        counter = counter + 1

camera = PiCamera()
warmUpCamera()
shutDownCamera()
