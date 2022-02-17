
# This script defines the steps to run the ai pipeline

print('AI Pipeline START')
import os
#### SETTING TENSORFLOW LOG LEVEL TO: WARNING
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from datasetmanipulation import *
from aimodelmanipulation import *

# Configuration for the histogram
display = True

# Folder from which to recover the files
path = 'DataCollected'


batchSize=100
validationBatchSize=50
steps_per_epoch=10
epochs=2
validation_steps=5

# Step 1 - Gather the data from the DataCollected folder
data = gatherImageData(path)

# Step 2 - Balance the data gathered against outliers.
# display=True, visualize a histogram of the data before and after the balancing
data = balanceDataset(data, numberOfBins=31, samplesPerBin=300, display=display)

# Step 3 - Split the data from the pandas format (used for balancing and visualization) into two lists for processing
imagePaths, steeringAngles = convertDataForProcessing(path, data)

# Step 4 - Split the dataset into training and validation datasets
trainingValue1, trainingValue2, validationValue1, validationValue2 = splitDataSet(imagePaths, steeringAngles)

# Step 5, 6 - Perform data Augmentation, Preprocess data
#imgBatch, steeringAnglesBatch = generateAugmentedTrainData(imagePaths, steeringAngles, batchSize=100)
augmentedTrainData = generateAugmentedTrainData(imagePaths, steeringAngles, batchSize=batchSize)
validationData = generateValidationData(imagePaths, steeringAngles, batchSize=validationBatchSize)

#imgBatchValidation, steeringAnglesBatchValidation = generateValidationData(imagePaths, steeringAngles, batchSize=50)

# Step 7 - Create Ai Model
model = createAiModel()

# Step 8 - Train Ai Model
#history = trainModel(model, imgBatch, steeringAnglesBatch, imgBatchValidation, steeringAnglesBatchValidation)
history = trainModel(model, augmentedTrainData, validationData, steps_per_epoch, epochs, validation_steps)

# Step 9 - Save the model
saveModel(model)

# Step 10
plotTrainingResults(history)

