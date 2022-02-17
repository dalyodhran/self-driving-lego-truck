import motor
import camera_module
import os
import pandas
from threading import Thread,Lock
import threading
import time


mutex = Lock()
collectionThread = Thread()

global imgList, steeringList
countFolder = 0
imgList = []
steeringList = []

myDirectory = os.path.join(os.getcwd(), 'DataCollected')
while os.path.exists(os.path.join(myDirectory, f'IMG{str(countFolder)}')):
    countFolder += 1
newPath = os.path.join(myDirectory, "IMG"+str(countFolder))
os.makedirs(newPath)

def collect_frames():
    t = threading.currentThread()
    while getattr(t, "run", True):
        collect_frame()
        #print("Hello")
        time.sleep(1)

def collect_frame():
    steering = motor.current_pos()
    frame_Path = camera_module.takeImg(newPath)
    imgList.append(frame_Path)
    steeringList.append(steering)


def save_collection():
    global imgList, steeringList
    rawData = {'Image': imgList,
               'Steering': steeringList}
    df = pandas.DataFrame(rawData)
    df.to_csv(os.path.join(
        myDirectory, f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Images: ', len(imgList))

def startCollecting():
    global collectionThread
    collectionThread = Thread(target=collect_frames)
    collectionThread.start()

def stopCollecting():
    global collectionThread
    collectionThread.run = False
    collectionThread.join()
    save_collection()
