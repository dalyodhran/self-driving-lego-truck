import tflite_runtime.interpreter as tflite
import os

if __name__ == "__main__":
    #motor.calibrate()
    model = tflite.load_model(os.path.join(os.getcwd(), './model.tflite'))
    print("loaded model")