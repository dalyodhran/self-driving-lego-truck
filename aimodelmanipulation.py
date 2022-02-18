
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D,Flatten,Dense
from tensorflow.keras.optimizers import Adam

#### Actually apply the data to train and validate the model
def trainModel(model, trainingData, validationData, steps_per_epoch, epochs, validation_steps):
    history = model.fit( trainingData,
                        steps_per_epoch=steps_per_epoch,
                        epochs=epochs,
                        validation_data=validationData,
                        validation_steps=validation_steps)
    return history

### Exponential linear units = 'elu', rectifier
# This model configuration is tuned as instructed by nvidia: 'Nvidia End-to-End Self-Driving Cars'
# https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf
def createAiModel():
  model = Sequential()

  # we will have to tinker with these values...
  # input shape = height, width, depth (color channels = RGB = 3), the input shape is 3 dimensional (h,w,depth)

  # Convolutional layers: recognizing features in images
  model.add(Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'))
  model.add(Convolution2D(36, (5, 5), (2, 2), activation='elu'))
  model.add(Convolution2D(48, (5, 5), (2, 2), activation='elu'))
  model.add(Convolution2D(64, (3, 3), activation='elu'))
  model.add(Convolution2D(64, (3, 3), activation='elu'))

  # Pooling Layer: compressing the output from the convolutional layer and flattening
  model.add(Flatten())

  # Fully connected layers
  model.add(Dense(100, activation = 'elu'))
  model.add(Dense(50, activation = 'elu'))
  model.add(Dense(10, activation = 'elu'))

  # output layer
  model.add(Dense(1))

  # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam
  optimizer = Adam(lr=0.0001)

  # loss quantifies how well a model is performing a task by calculating a single number, the loss,
  # from the model output and the desired target.
  # If the model predictions are totally wrong, the loss will be a high number.
  # If they’re pretty good, it will be close to zero.
  model.compile(optimizer,loss='mse')

  model.summary()
  return model

def saveModel(model):
    model.save('model.h5')
    print('Model Saved')

def getPrediction(model, img):
    value = float(model.predict(img))
    #print(value)
    return value

