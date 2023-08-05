import math
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime
from gimmick import constants
from gimmick.models.autoencoder import AutoEncoder


class Model(AutoEncoder):
    """ This algorithm uses a LSTM based encoder-decoder n/w for learning and generating images.
    https://en.wikipedia.org/wiki/Long_short-term_memory
    """

    def build_model_graph(self, images_shape):
        total_pixels = images_shape[0] * images_shape[1] * images_shape[2]

        num_encoder_layers = int(math.log(images_shape[0], 2)) - 2 if self.num_encoder_layers == 'auto' else int(self.num_encoder_layers)
        num_encoder_layers = max(num_encoder_layers, 3)

        num_decoder_layers = int(math.log(images_shape[0], 2))- 2 if self.num_decoder_layers == 'auto' else int(self.num_decoder_layers)
        num_decoder_layers = max(num_decoder_layers, 3)

        log2_code = int(math.log(self.code_length, 2))
        print("num_enoder_layer:\t", num_encoder_layers)
        print("num_decoder_layers:\t", num_decoder_layers)
        print("log2_code:\t\t", log2_code)

        model = keras.Sequential(name="autoencoder_lstm")
        model.add(layers.InputLayer(input_shape=images_shape))
        model.add(layers.Reshape((images_shape[0], images_shape[1] * images_shape[2])))

        # Encoder Layer
        for i in range(1, num_encoder_layers + 1):
            neurons = 2 ** (num_encoder_layers - i + log2_code + 1) # Encoder layer size will be always greater then code_length by multiple of 2
            return_sequences = True if i < num_decoder_layers else False # In Last layer we do not return sequences
            model.add(layers.LSTM(neurons, activation='relu', return_sequences=return_sequences, name="encoder_layer_" + str(i) ))

        # Code Layer
        model.add(layers.Dense(self.code_length, name="code"))
        model.add(layers.Reshape((2, int(self.code_length/2) )))

        # Decoder Layer
        for i in range(1, num_decoder_layers + 1):
            neurons = 2 ** (i + log2_code)  # Decoder layer size will be always greater then code_length by multiple of 2
            return_sequences = True if i < num_decoder_layers else False # In Last layer we do not return sequences
            model.add(layers.LSTM(neurons, activation="relu", return_sequences=return_sequences, name="decoder_layer_" + str(i) ))

        model.add(layers.Dense(total_pixels, activation="relu", name="final_layer"))
        model.add(layers.Reshape(images_shape))

        optimizer =self.optimizer
        optimizer.learning_rate = self.learning_rate

        model.compile(optimizer=optimizer, loss=self.loss_function, metrics=self.metrics)

        print(model.summary())
        self.model = model

        def _code_generator_model():
            layers_ = [layers.InputLayer(input_shape=images_shape), layers.Reshape((images_shape[0], images_shape[1] * images_shape[2]))]
            encoder_layers = [layer.name if 'encoder_layer' in layer.name else None for layer in model.layers]
            num_encoder_layers = len(list(filter(lambda x: x, encoder_layers))) + 2 # 1 Each for (Flatten, Reshape, Code) layer
            layers_.extend(model.layers[:num_encoder_layers])  # Trim all layers except encoder layers

            model_code_generator = keras.Sequential(layers_)
            model_code_generator.build((None, images_shape[0], images_shape[1], images_shape[2]))

            for layer in model_code_generator.layers:
                if list(filter(lambda x: x in layer.name, ['flatten', 'reshape'])):
                    continue
                assert all([np.array_equal(layer.get_weights()[0], model.get_layer(layer.name).get_weights()[0]),
                            np.array_equal(layer.get_weights()[1], model.get_layer(layer.name).get_weights()[1])]),  "%s weights not same" % layer.name

            print(model_code_generator.summary())
            return model_code_generator

        self.model_code_generator = _code_generator_model()

        def _image_generator_model():
            encoder_layers = [layer.name if 'encoder_layer' in layer.name else None for layer in model.layers]
            num_encoder_layers = len(list(filter(lambda x: x, encoder_layers))) + 2 # 1 Each for (Flatten, Reshape, Code) layer

            # Building model
            model_image_generator = keras.Sequential(model.layers[num_encoder_layers:])
            model_image_generator.build((None, self.code_length))
            print(model_image_generator.summary())
            return model_image_generator

        self.model_image_generator = _image_generator_model()
