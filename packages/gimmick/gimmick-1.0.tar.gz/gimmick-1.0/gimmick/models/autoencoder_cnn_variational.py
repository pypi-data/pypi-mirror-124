import math
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from gimmick import constants
from gimmick.models.autoencoder import AutoEncoder

class Model(AutoEncoder):
    """ This algorithm uses a CNN based variational autoenocder for learning and generating images.
    https://en.wikipedia.org/wiki/Variational_autoencoder
    """

    def build_model_graph(self, images_shape):
        print(self.__dict__)
        total_pixels = images_shape[0] * images_shape[1] * images_shape[2]

        num_encoder_layers = int(math.log(images_shape[0], 2)) - 2 #if self.num_encoder_layer == "auto" else int(self.num_encoder_layer)
        num_decoder_layers = int(math.log(images_shape[0], 2)) - 2 #if self.num_decoder_layers == "auto" else int(self.num_decoder_layers)

        log2_code = int(math.log(self.code_length, 2))
        print("num_enoder_layer:\t", num_encoder_layers)
        print("num_decoder_layers:\t", num_decoder_layers)
        print("log2_code:\t\t", log2_code)

        filter_size = (3, 3)
        pool_size = (2, 2)

        def _encoder(x):
            # x = layers.Reshape((images_shape[0], images_shape[1], images_shape[2]))(x)

            # Encoder Layer
            for i in range(1, num_encoder_layers + 1):
                neurons = 2 ** (num_encoder_layers - i + log2_code + 1) # Encoder layer size will be always greater then code_length by multiple of 2

                if i == 1 and images_shape[0] <= 16:
                    x = layers.Conv2D(neurons, filter_size, activation='relu', padding='same', strides=1, name="encoder_layer_extra1")(x)
                if i == 1 and images_shape[0] <= 8:
                    x = layers.Conv2D(neurons, filter_size, activation='relu', padding='same', strides=1, name="encoder_layer_extra2")(x)
                x = layers.Conv2D(neurons, filter_size, activation='relu', padding='same', strides=2, name="encoder_layer_" + str(i) )(x)

            # Code Layer
            x = layers.Flatten()(x)
            return x

        def _decoder(code):

            x = layers.Reshape((2, 2, int(self.code_length / 4)))(code)

            # Decoder Layer
            for i in range(1, num_decoder_layers + 1):
                neurons = 2 ** (i + log2_code)  # Decoder layer size will be always greater then code_length by multiple of 2

                if i == 1 and images_shape[0] <= 16:
                    x = layers.Conv2DTranspose(neurons, filter_size, activation='relu', padding='same', strides=1, name="decoder_layer_extra1" )(x)
                if i == 1 and images_shape[0] <= 8:
                    x = layers.Conv2DTranspose(neurons, filter_size, activation='relu', padding='same', strides=1, name="decoder_layer_extra2" )(x)
                x = layers.Conv2DTranspose(neurons, filter_size, activation='relu', padding='same', strides=2, name="decoder_layer_" + str(i) )(x)

            output = layers.Conv2DTranspose(images_shape[2], filter_size, activation='relu', padding='same', strides=2, name='decoder_layer_%s' % str(i + 1) )(x)
            return output

        input = keras.Input(shape=images_shape)

        x = _encoder(input)

        mean = layers.Dense(self.code_length, name='mean')(x)
        std = keras.activations.softplus(layers.Dense(self.code_length, name='std')(x))

        # Reparametrization trick
        epsilon = tf.random.normal(tf.stack([tf.shape(x)[0], self.code_length]), name='epsilon')
        code = tf.add(mean, epsilon * std, name='code')

        output = _decoder(code)

        optimizer =self.optimizer
        optimizer.learning_rate = self.learning_rate

        model = tf.keras.Model(inputs=input, outputs=output)
        model.compile(optimizer=optimizer, loss=self.loss_function, metrics=self.metrics)
        self.model = model

        print(model.summary())
        print("============================================================")

        def _code_generator_model():
            # Building model which generate code statistics
            model_code_generator = tf.keras.Model(inputs=input, outputs=code)
            model_code_generator.build((None, images_shape[0], images_shape[1], images_shape[2]))
            print(model_code_generator.summary())
            return model_code_generator

        self.model_code_generator = _code_generator_model()

        print("============================================================")
        def _image_generator_model():
            generator_layer_num = 0
            for cntr, layer in enumerate(model.layers):
                if layer.name == 'tf_op_layer_code':
                    break
                generator_layer_num += 1

            # Building model which generate images
            model_image_generator = keras.Sequential(model.layers[generator_layer_num+1:])
            model_image_generator.build((None, self.code_length))
            print(model_image_generator.summary())
            return model_image_generator

        self.model_image_generator = _image_generator_model()
