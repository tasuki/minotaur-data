import h5py
import numpy as np

from keras.models import load_model
from keras_resnet import custom_objects

from .results import order, rotate
from munch.converter import convert_record

network = 'nn/01_first_nn.h5'
model = load_model(network)

def predict(game_record):
    moves = game_record.split(';')
    nparr = np.array([convert_record(moves)])
    predictions = order(model.predict(nparr)[0].tolist())

    if len(moves) % 2 == 1:
        predictions = [rotate(p) for p in predictions]

    return predictions
