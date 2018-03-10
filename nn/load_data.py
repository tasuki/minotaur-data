import numpy as np
import h5py

def get_data(fname, classes):
    data = h5py.File(fname)
    return np.array(data["x"]), np.array(data["y"]).reshape(len(data["y"]), classes)

def get_train(classes):
    return get_data("../data/records-1-train.h5", classes)

def get_valid(classes):
    return get_data("../data/records-2-valid.h5", classes)

def get_test(classes):
    return get_data("../data/records-3-test.h5", classes)
