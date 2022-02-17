
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
# This model configuration is tuned as instructed by nvidia
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
  model.add(Dense(100, activation = 'elu'))
  model.add(Dense(50, activation = 'elu'))
  model.add(Dense(10, activation = 'elu'))
  model.add(Dense(1))

  # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam
  optimizer = Adam(learning_rate=0.0001)
  model.compile(optimizer,loss='mse')
  model.summary()
  return model

def saveModel(model):
    model.save('model.h5')
    print('Model Saved')
