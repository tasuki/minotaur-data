import os

import numpy as np
import keras.layers
import keras.utils.np_utils
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
import keras_resnet.models

from load_data import get_train, get_valid

fname = os.path.basename(__file__)[:-3]

shape, classes = (6, 9, 9), 3*9*9
inp = keras.layers.Input(shape)

model = keras_resnet.models.ResNet34(inp, classes=classes)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

x_train, y_train = get_train(classes)
x_valid, y_valid = get_valid(classes)

lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
early_stopper = EarlyStopping(monitor='val_loss', min_delta=0.001, patience=1)
csv_logger = CSVLogger(fname + '.csv')

model.fit(
    x_train,
    y_train,
    batch_size=1024,
    epochs=10,
    validation_data=(x_valid, y_valid),
    shuffle=True,
    callbacks=[lr_reducer, early_stopper, csv_logger]
)

model.save(fname + '.h5')
