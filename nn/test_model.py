from keras.models import load_model
from keras.utils import plot_model

network = '01_first_nn.h5'
model = load_model(network)

#plot_model(model, show_shapes=True, show_layer_names=True, to_file='model.png')
f = open('model.yml', 'w')
f.write(model.to_yaml())
