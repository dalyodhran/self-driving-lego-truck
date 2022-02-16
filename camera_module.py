from picamera import PiCamera
from datetime import datetime
from pathlib import Path

camera = PiCamera()

def takeImg(savePath=str(Path().absolute()) + "/"):
    warmUpCamera()
    timeNow = datetime.now().strftime("%H_%M_%S")
    imageFileName = "image_" + timeNow + ".jpg"
    camera.capture(savePath + imageFileName, resize=(480, 240))
    shutDownCamera()
    return savePath + imageFileName

def warmUpCamera():
    camera.start_preview()
    camera.resolution = (852, 480)

def shutDownCamera():
    camera.stop_preview()

if __name__ == '__main__':
    counter = 0
    while (counter < 10)
        takeImg()
        counter = counter + 1
