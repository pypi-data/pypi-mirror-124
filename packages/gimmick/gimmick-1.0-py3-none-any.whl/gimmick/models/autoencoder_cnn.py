import math
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from datetime import datetime
from gimmick import constants
from gimmick.models.autoencoder import AutoEncoder


class Model(AutoEncoder):
    """ This algorithm uses a CNN based encoder-decoder n/w for learning and generating images.
    https://en.wikipedia.org/wiki/Convolutional_neural_network
    """
    def build_model_graph(self, images_shape):
        total_pixels = images_shape[0] * images_shape[1] * images_shape[2]

        num_encoder_layers = int(math.log(images_shape[0], 2)) - 2 #if self.num_encoder_layer == "auto" else int(self.num_encoder_layer)
        num_decoder_layers = int(math.log(images_shape[0], 2)) - 2 #if self.num_decoder_layers == "auto" else int(self.num_decoder_layers)

        log2_code = int(math.log(self.code_length, 2))
        print("num_enoder_layer:\t", num_encoder_layers)
        print("num_decoder_layers:\t", num_decoder_layers)
        print("log2_code:\t\t", log2_code)

        model = keras.Sequential(name="autoencoder_cnn")
        model.add(layers.InputLayer(input_shape=images_shape))
        model.add(layers.Reshape((images_shape[0], images_shape[1], images_shape[2])))

        filter_size = (3, 3)
        pool_size = (2, 2)

        # Encoder Layer
        for i in range(1, num_encoder_layers + 1):
            neurons = 2 ** (num_encoder_layers - i + log2_code + 1) # Encoder layer size will be always greater then code_length by multiple of 2

            #model.add(layers.Conv2D(neurons, filter_size, activation='relu', padding='same', name="encoder_layer_" + str(i) ))
            #model.add(layers.MaxPooling2D(pool_size=pool_size, padding='same'))

            if i == 1 and images_shape[0] <= 16:
                model.add(layers.Conv2D(neurons, filter_size, activation='relu', padding='same', strides=1, name="encoder_layer_extra1"))
            if i == 1 and images_shape[0] <= 8:
                model.add(layers.Conv2D(neurons, filter_size, activation='relu', padding='same', strides=1, name="encoder_layer_extra2"))
            model.add(layers.Conv2D(neurons, filter_size, activation='relu', padding='same', strides=2, name="encoder_layer_" + str(i) ))

        # Code Layer
        model.add(layers.Flatten())
        model.add(layers.Dense(self.code_length, name="code"))
        model.add(layers.Reshape((2, 2, int(self.code_length / 4) )))

        # Decoder Layer
        for i in range(1, num_decoder_layers + 1):
            neurons = 2 ** (i + log2_code)  # Decoder layer size will be always greater then code_length by multiple of 2

            #model.add(layers.Conv2D(neurons, filter_size, activation='relu', padding='same', name="decoder_layer_" + str(i) ))
            #model.add(layers.UpSampling2D(size=pool_size, interpolation='nearest'))

            if i == 1 and images_shape[0] <= 16:
                model.add(layers.Conv2DTranspose(neurons, filter_size, activation='relu', padding='same', strides=1, name="decoder_layer_extra1" ))
            if i == 1 and images_shape[0] <= 8:
                model.add(layers.Conv2DTranspose(neurons, filter_size, activation='relu', padding='same', strides=1, name="decoder_layer_extra2" ))
            model.add(layers.Conv2DTranspose(neurons, filter_size, activation='relu', padding='same', strides=2, name="decoder_layer_" + str(i) ))

        #model.add(layers.Conv2D(images_shape[2], filter_size, activation='relu', padding='same', name="decoder_layer_" + str(i + 1) ))
        #model.add(layers.UpSampling2D(size=pool_size, interpolation='nearest'))
        model.add(layers.Conv2DTranspose(images_shape[2], filter_size, activation='relu', padding='same', strides=2, name='decoder_layer_%s' % str(i + 1) ))

#         model.add(layers.Flatten())
#         model.add(layers.Dropout(0.5))
#         model.add(layers.Dense(total_pixels, activation="relu", name="final_layer"))
#         model.add(layers.Reshape(images_shape))

        optimizer =self.optimizer
        optimizer.learning_rate = self.learning_rate

        model.compile(optimizer=optimizer, loss=self.loss_function, metrics=self.metrics)
        print(model.summary())
        self.model = model


        def _code_generator_model():

            layers_ = [layers.InputLayer(input_shape=images_shape), layers.Reshape((images_shape[0], images_shape[1] * images_shape[2]))]

            num_encoder_layers = len(layers_) - 1
            for layer in model.layers:
                if layer.name == "code":
                    break
                num_encoder_layers += 1

            layers_.extend(model.layers[:num_encoder_layers])  # Trim all layers except encoder layers

            model_code_generator = keras.Sequential(layers_)
            model_code_generator.build((None, images_shape[0], images_shape[1], images_shape[2]))

            for layer in model_code_generator.layers:
                if list(filter(lambda x: x in layer.name, ['flatten', 'reshape', 'max_pooling'])):
                    continue
                assert all([np.array_equal(layer.get_weights()[0], model.get_layer(layer.name).get_weights()[0]),
                            np.array_equal(layer.get_weights()[1], model.get_layer(layer.name).get_weights()[1])]),  "%s weights not same" % layer.name

            print(model_code_generator.summary())
            return model_code_generator
        self.model_code_generator = _code_generator_model()

        def _image_generator_model():
            num_encoder_layers = 1
            for layer in model.layers:
                if layer.name == "code":
                    break
                num_encoder_layers += 1

            # Building model
            model_image_generator = keras.Sequential(model.layers[num_encoder_layers:])
            model_image_generator.build((None, self.code_length))
            return model_image_generator
        self.model_image_generator = _image_generator_model()
