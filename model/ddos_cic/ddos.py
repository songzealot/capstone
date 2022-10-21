from keras.models import load_model
import os

import numpy as np

model_path = os.path.dirname(os.path.realpath(__file__)) + "/0907.h5"
model = load_model(model_path)

detection_standard = 0.5


def ddos(data):
    data = list(map(float, data))
    data = np.array(data)
    data = np.reshape(data, (1, 1, 21))
    model_result = model.predict(data)
    model_result = model_result.tolist()
    model_result = model_result[0][0]

    if (detection_standard < model_result) and (model_result <= 1):
        detection_result = 1
    elif (0 <= model_result) and (model_result <= detection_standard):
        detection_result = 0
    else:
        # 뭔가 잘못됨
        detection_result = -1
    return detection_result
