print('Setting UP')
import os
#### SETTING TENSORFLOW LOG LEVEL TO: WARNING
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from sklearn.model_selection import train_test_split
from utlis import *


#### STEP 1 - INITIALIZE DATA (RETURNS PANDAS DATAFRAME FORMAT)
path = 'DataCollected'
data = importDataInfo(path)

#### Print a small summary of the data collected (top 5 elements)
print(data.head())

#### STEP 2 - VISUALIZE HISTOGRAM AND BALANCE DATA
#### Balancing happens by way of removing unnecessary samples from the dataset (just the paths and corresponding
#### steering angles from each list) in order to even out the data and give more significance to all the other angles
data = balanceData(data,display=True)

#### STEP 3 - PREPARE FOR PROCESSING
#### Split the data from the pandas format (used for balancing and visualization) into two lists for processing
imagesPath, steerings = loadData(path,data)

#### STEP 4 - SPLIT FOR TRAINING AND VALIDATION
#### Basically what this is doing is splitting the single dataset between two buckets:
#### Test bucket: Used for testing the model, once it has been trained
#### Train bucket: Used for training the model
#### That is being done with this function from the sckit library
#### test_size represent the percentage of data used for testing and random state
xTrain, xVal, yTrain, yVal = train_test_split(imagesPath, steerings,
                                              test_size=0.2,random_state=10)
print('Total Training Images: ',len(xTrain))
print('Total Validation Images: ',len(xVal))

#### STEP 5 - AUGMENT DATA
#### this step is included in data generation (dataGen) perform in the training step

#### STEP 6 - PREPROCESS
#### this step is included in data generation (dataGen) perform in the training step

#### STEP 7 - CREATE MODEL
model = createModel()

#### STEP 8 - TRAINING
#### Actually apply the data to train and validate the model
#### the first parameter is the training data
history = model.fit(dataGen(xTrain, yTrain, 100, trainFlag=1),
                                  steps_per_epoch=100,
                                  epochs=10,
                                  validation_data=dataGen(xVal, yVal, 50, 0),
                                  validation_steps=50)

#### STEP 9 - SAVE THE MODEL
model.save('model.h5')
print('Model Saved')

#### STEP 10 - PLOT THE RESULTS
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()


