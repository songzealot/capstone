import tensorflow as tf
import pandas as pd
import model.probe_dnn.label as label
import os

# 모델 로드
feature_names = []
fn_path = os.path.dirname(os.path.realpath(__file__)) + "/Field_Names.txt"
with open(fn_path, "r") as f:
    for line in f.readlines()[0:]:
        name, __ = line.strip()[:-1].split(":")
        feature_names.append(name)

path = os.path.dirname(os.path.realpath(__file__)) + "/dos_model.h5"
model = tf.keras.models.load_model(path)


def dos_model(data):
    # DoS 모델
    df = pd.DataFrame(columns=feature_names)
    if isinstance(data, list):
        df.loc[0] = data
    elif isinstance(data, pd.DataFrame):
        df = data
        df.columns = feature_names
    else:
        print("list나 DataFrame으로 넣어주세요")
        return

    df2 = label.trans(df)
    prec = model.predict(df2.df, verbose=0)
    threshold = 0.9
    prec2 = 1 if prec[0][0] > threshold else 0
    df = df.drop([0], axis=0)
    return prec2
