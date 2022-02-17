import motor
import camera_module
import os
import pandas as pd

global imgList, steeringList
countFolder = 0
imgList = []
steeringList = []

myDirectory = os.path.join(os.getcwd(), 'DataCollected')
while os.path.exists(os.path.join(myDirectory, f'IMG{str(countFolder)}')):
    countFolder += 1
newPath = myDirectory + "/IMG"+str(countFolder)
os.makedirs(newPath)


def collect_frame():
    steering = motor.current_pos()
    frame_Path = camera_module.takeImg(newPath)
    imgList.append(frame_Path)
    steeringList.append(steering)


def save_collection():
    global imgList, steeringList
    rawData = {'Image': imgList,
               'Steering': steeringList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(
        myDirectory, f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Images: ', len(imgList))
