from keras.models import model_from_json
import numpy as np
import cv2

class PredictLandmark():
    def __init__(self, parent=None):
        pass

    def setImageSize(self, _width, _height):
        self.input_size = np.array([_height, _width])

    def calcImageRatio(self, _width, _height):
        wRatio = _width / self.input_size[1]
        hRatio = _height / self.input_size[0]
        self.size_ratio = np.array([hRatio, wRatio])

    def setModel(self, model_path):
        json_name = '{0}/architecture.json'.format(model_path)
        weights_name = '{0}/weights.h5'.format(model_path)
        self.model = model_from_json(open(json_name).read())
        self.model.load_weights(weights_name)

    def getLandmarkPos(self, src):
        img = src
        if len(src.shape) == 3:
            img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (self.input_size[1], self.input_size[0]))
        img = img / 255
        X = img.reshape(-1, self.input_size[0], self.input_size[1], 1)

        y = self.model.predict(X)[0]

        half_size = self.input_size.max() / 2
        posX = (y[0::2] * half_size + half_size) * self.size_ratio[1] + 0.5
        posY = (y[1::2] * half_size + half_size) * self.size_ratio[0] + 0.5

        return posX, posY