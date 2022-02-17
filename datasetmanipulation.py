
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.utils import shuffle
import cv2
import random
import os
import matplotlib.image as mpimg
# Used for image augmentation
from imgaug import augmenters as iaa

from datavisualization import *

# This performs the actual import of the real data, from the given file paths, in the validation dataset
def generateAugmentedTrainData(imagesPath, steeringAnglesList, batchSize):
    while True:
        imgBatch = []
        steeringBatch = []

        for i in range(batchSize):
            index = random.randint(0, len(imagesPath) - 1)
            img, steering = augmentImage(imagesPath[index], steeringAnglesList[index])
            img = preProcess(img)
            imgBatch.append(img)
            steeringBatch.append(steering)
        yield (np.asarray(imgBatch),np.asarray(steeringBatch))

# This performs the actual import of the real data, from the given file paths, in the training dataset
# for dataset augmentation
def generateValidationData(imagesPath, steeringAnglesList, batchSize):
    while True:
        imgBatch = []
        steeringBatch = []

        for i in range(batchSize):
            index = random.randint(0, len(imagesPath) - 1)
            img = mpimg.imread(imagesPath[index])
            steering = steeringAnglesList[index]
            img = preProcess(img)
            imgBatch.append(img)
            steeringBatch.append(steering)
        yield (np.asarray(imgBatch),np.asarray(steeringBatch))

# Pre-process the image according to nvidia recommendation
# Change color space to YUV (luma-chroma) color space from RGB
# Slightly blur the image
# Resize the image to be 200 x 66
def preProcess(img):
    img = img[54:120,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img

# Randomly affects the images dataset (panning around, flipping the image, changing the brightness etc...)
# is a step needed to artificially broaden the dataset when training the model
def augmentImage(imgPath,steering):
    img = mpimg.imread(imgPath)
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})
        img = pan.augment_image(img)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1, 1.2))
        img = zoom.augment_image(img)
    if np.random.rand() < 0.5:
        brightness = iaa.Multiply((0.5, 1.2))
        img = brightness.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)
        steering = -steering
    return img, steering

# Convert back from the pandas DataFrame format to arrays
def convertDataForProcessing(path, data):
    imagesPath = []
    steeringAngles = []
    for i in range(len(data)):
        indexed_data = data.iloc[i]
        imagesPath.append(os.path.join(path, indexed_data[0]))
        steeringAngles.append(float(indexed_data[1]))
    imagesPath = np.asarray(imagesPath)
    steeringAngles = np.asarray(steeringAngles)
    return imagesPath, steeringAngles


# Import the image data (the captures from the collection phase) into the pandas DataFrame format
def gatherImageData(path):
    columns = ['ImagePath', 'SteeringAngles']
    noOfFolders = len(os.listdir(path))//2
    data = pd.DataFrame()
    for x in range(0,noOfFolders):
        dataNew = pd.read_csv(os.path.join(path, f'log_{x}.csv'), names = columns)
        print(f'{x}:{dataNew.shape[0]} ',end='')
        dataNew['ImagePath']=dataNew['ImagePath'].apply(getRelativePath)
        data =data.append(dataNew,True)
    print(' ')
    print('Total Images Imported',data.shape[0])

    #### Print a small summary of the data collected (top 5 elements)
    print(data.head())

    return data

def getRelativePath(filePath):
    myImagePathL = filePath.split('/')[-2:]
    myImagePath = os.path.join(myImagePathL[0],myImagePathL[1])
    return myImagePath

# Basically what this is doing is splitting the single dataset between two buckets:
# Test bucket: Used for testing the model, once it has been trained
# Train bucket: Used for training the model
# That is being done with this function from the sckit library
# test_size represent the percentage of data, from the single dataset, to be used for testing and random state
def splitDataSet(imagesPath, steeringAngles):
    trainingValue1, trainingValue2, validationValue1, validationValue2 = train_test_split(imagesPath, steeringAngles,
                                              test_size=0.2,random_state=10)
    return trainingValue1, trainingValue2, validationValue1, validationValue2

# Balancing happens by way of removing unnecessary samples from the dataset (just the paths and corresponding
# steering angles from each list) in order to even out the data and give more significance to all the other steering
# angle values.
# The number of samples to keep for each bin is strictly related to the amount of pictures captured per "scenario"
# assuming 500(ish) pictures taken in each and every data collection "pass"
def balanceDataset(data, numberOfBins, samplesPerBin, display):
    hist, bins = np.histogram(data['SteeringAngles'], numberOfBins)
    if display:
        center = (bins[:-1] + bins[1:]) * 0.5
        plt.bar(center, hist, width=0.03)
        plt.plot((np.min(data['SteeringAngles']), np.max(data['SteeringAngles'])), (samplesPerBin, samplesPerBin))
        plt.title('Data Visualisation')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        plt.show()
    removeindexList = []
    for j in range(numberOfBins):
        binDataList = []
        for i in range(len(data['SteeringAngles'])):
            if data['SteeringAngles'][i] >= bins[j] and data['SteeringAngles' ][i] <= bins[j + 1]:
                binDataList.append(i)
        binDataList = shuffle(binDataList)
        binDataList = binDataList[samplesPerBin:]
        removeindexList.extend(binDataList)

    print('Removed Images:', len(removeindexList))
    data.drop(data.index[removeindexList], inplace=True)
    print('Remaining Images:', len(data))

    if display:
        hist, _ = np.histogram(data['SteeringAngles'], (numberOfBins))
        plt.bar(center, hist, width=0.03)
        plt.plot((np.min(data['SteeringAngles']), np.max(data['SteeringAngles'])), (samplesPerBin, samplesPerBin))
        plt.title('Balanced Data')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        plt.show()
    return data

def plotTrainingResults(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(['Training', 'Validation'])
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.show()
