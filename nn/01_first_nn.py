import h5py
import numpy as np

import keras.layers
import keras.utils.np_utils
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping

import keras_resnet.models

shape, classes = (6, 9, 9), 3*9*9
inp = keras.layers.Input(shape)

model = keras_resnet.models.ResNet18(inp, classes=classes)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

def get_x_y(data, classes):
    return np.array(data["x"]), np.array(data["y"]).reshape(len(data["y"]), classes)

train_data = h5py.File("../data/records-1-train.h5")
x_train, y_train = get_x_y(train_data, classes)

valid_data = h5py.File("../data/records-2-valid.h5")
x_valid, y_valid = get_x_y(valid_data, classes)

test_data = h5py.File("../data/records-3-test.h5")
x_valid, y_valid = get_x_y(valid_data, classes)


lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
early_stopper = EarlyStopping(min_delta=0.001, patience=10)
csv_logger = CSVLogger('01_first_nn.csv')

model.fit(
    x_train,
    y_train,
    batch_size=128,
    epochs=10,
    validation_data=(x_valid, y_valid),
    shuffle=True,
    callbacks=[lr_reducer, early_stopper, csv_logger]
)

model.save('01_first_nn_10_epochs.h5')
