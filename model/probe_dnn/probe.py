import tensorflow as tf
import pandas as pd
import model.probe_dnn.label as label
import os

cols = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "count",
    "serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
]
# 모델 로드
feature_names = []
fn_path = os.path.dirname(os.path.realpath(__file__)) + "/Field_Names.txt"
with open(fn_path, "r") as f:
    for line in f.readlines()[0:]:
        name, __ = line.strip()[:-1].split(":")
        feature_names.append(name)

path = os.path.dirname(os.path.realpath(__file__)) + "/DNN_150000.h5"
model = tf.keras.models.load_model(path)


def probe_model(data):
    # Probe 모델
    df = pd.DataFrame(columns=feature_names)
    if isinstance(data, list):
        df.loc[0] = data
    elif isinstance(data, pd.DataFrame):
        df = data
        df.columns = feature_names
    else:
        print("list나 DataFrame으로 넣어주세요")
        return

    for c in feature_names:
        if c not in cols:
            df = df.drop(c, axis=1)

    df2 = label.trans(df)
    prec = model.predict(df2.df)
    threshold = 0.5
    prec2 = 1 if prec[0][0] > threshold else 0
    df = df.drop([0], axis=0)
    return prec2
