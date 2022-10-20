from keras.models import load_model
import os

import numpy as np

model_path = os.path.dirname(os.path.realpath(__file__)) + "/LSTM_250000.h5"

model = load_model(model_path)

detection_standard = 0.5


def bruteForce(data):
    # print(f"리스트: {data}")
    # for i in data:
    #     print(type(i))
    # data = list(map(float, data))
    # print(f"플로트: {data}")
    data = np.array(data)
    # print(data)
    data = np.reshape(data, (1, 1, 21))
    # print(data)
    model_result = model.predict(data)
    model_result = model_result.tolist()
    model_result = model_result[0][0]

    print(model_result)

    if (detection_standard < model_result) and (model_result <= 1):
        detection_result = 1
    elif (0 <= model_result) and (model_result <= detection_standard):
        detection_result = 0
    else:
        # 뭔가 잘못됨
        detection_result = -1
    return detection_result
