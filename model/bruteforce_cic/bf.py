from keras.models import load_model
import os
import numpy as np

# 모델 로드
model_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/model_bruteforce_remake_ver2.h5"
)
model = load_model(model_path)

# 공격 판정 기준치
detection_standard = 0.5


def bruteForce(data):
    # Brute Force 모델
    data = np.array(data)
    data = np.reshape(data, (1, 1, 21))
    model_result = model.predict(data, verbose=0)
    model_result = model_result.tolist()
    model_result = model_result[0][0]

    if (detection_standard < model_result) and (model_result <= 1):
        # 공격
        detection_result = 1
    elif (0 <= model_result) and (model_result <= detection_standard):
        # 정상
        detection_result = 0
    else:
        # 뭔가 잘못됨
        detection_result = -1
    return detection_result
