import h5py
import numpy as np

from keras.models import load_model
from keras_resnet import custom_objects

test_records = '../data/records-3-test.h5'
network = '02_resnet34_10ep_58pc.h5'
sample = 95

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

def get_samples(data, from_sample=0, to_sample=None):
    if to_sample == None:
        to_sample = len(data) - from_sample
    x = np.array(data['x'][from_sample:to_sample])
    y = np.array(data['y'][from_sample:to_sample])
    return x, y

def get_sample(data, sample):
    return get_samples(data, sample, sample + 1)

def debug_sample(x, expected, predicted):
    print(x)
    print()
    print('---')
    print()
    print(expected)
    print()
    print('---')
    print()
    print(predicted)

def is_correct(expected, actual):
    chosen = np.zeros(actual.shape)
    chosen[np.unravel_index(actual.argmax(), actual.shape)] = 1

    return np.array_equal(chosen, expected)

model = load_model(network, custom_objects=custom_objects)
test_data = h5py.File(test_records)

x, y = get_sample(test_data, sample)
predictions = model.predict(x).reshape(len(x), 3, 9, 9)

debug_sample(x[0], y[0], predictions[0])
if is_correct(y[0], predictions[0]):
    print("predicted correctly")
else:
    print("predicted wrong")
