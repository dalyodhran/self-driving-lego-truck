from aimodelmanipulation import *
from datasetmanipulation import *
from tensorflow.keras.models import load_model
import cv2
import numpy as np

data = gatherImageData('DataCollected',7,8)
model = load_model('/Users/mcoletta/FunProjs/hackathon/self-driving-lego-truck/model.h5')

imagepaths = list(data['ImagePath'])

def getImg(path):
    img = cv2.imread(path)
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    return img

def getPredictionForList(model, paths):
    predictions = []
    for p in paths:
        p = os.path.join('DataCollected', p)
        img = getImg(p)
        predictions.append(getPrediction(model, img))
    return predictions

predictions = list(getPredictionForList(model, imagepaths))
data['Predictions'] = predictions
#print(data)
data.to_csv(f'predictions.csv')

