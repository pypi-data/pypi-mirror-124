import json
import logging
from threading import Thread

import requests

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse


import tensorflow as tf

from tensorflow.python.keras import backend as K
from tensorflow.python.keras.layers import Lambda

def recall_N(y_true, y_pred, N=50):
    return len(set(y_pred[:N]) & set(y_true)) * 1.0 / len(y_true)

def sampledsoftmaxloss(y_true, y_pred):
    return K.mean(y_pred)

def get_item_embedding(item_embedding, item_input_layer):
    return Lambda(lambda x: tf.squeeze(tf.gather(item_embedding, x), axis=1))(
        item_input_layer)