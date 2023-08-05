import os
import math
import time
import pickle
import shutil
import random
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from tqdm import tqdm
from datetime import datetime
from sklearn.model_selection import train_test_split
from gimmick import constants

class Generator():
    def __init__(self, optimizer, learning_rate, num_layers=None):
        super(Generator, self).__init__()

        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.num_layers = num_layers

    def build_graph(self, images_shape, code_length, hidden_dim):
        '''
        Generator Class
        Parameters:
            code_length: the dimension of the noise vector, a scalar
            total_image_pixels: the dimension of the images, fitted for the dataset used, a scalar
              (MNIST images are 28 x 28 = 784 so that is your default)
            hidden_dim: the inner dimension, a scalar
        '''
        print("======================================= Generator =========================================")
        total_image_pixels = np.prod(images_shape)
        model = keras.Sequential(name="generator")
        model.add(layers.InputLayer(input_shape=code_length))

        num_layers = self.num_layers if self.num_layers else max( 3, int(total_image_pixels / hidden_dim) - 1)
        print('layers', num_layers)

        for i in range(num_layers - 1):
            model.add(layers.Dense(hidden_dim * i, name="generator_layer_" + str(i)))
            model.add(layers.BatchNormalization())
            model.add(layers.Activation('relu'))

        model.add(layers.Dense(total_image_pixels, name="generator_layer_last" + str(i)))
        #model.add(layers.BatchNormalization())
        model.add(layers.Activation('sigmoid'))
        model.add(layers.Reshape(images_shape))

        self.optimizer.learning_rate = self.learning_rate
        #model.compile(optimizer=self.generator_optimizer, loss=self.loss_function, metrics=self.metrics)
        print(model.summary())
        self.model = model

class Discriminator():
    def __init__(self, optimizer, learning_rate, num_layers=None):
        super(Discriminator, self).__init__()

        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.num_layers = num_layers

    def build_graph(self, images_shape, hidden_dim):
        '''
        Discriminator Class
        Parameters:
            code_length: the dimension of the noise vector, a scalar
            total_image_pixels: the dimension of the images, fitted for the dataset used, a scalar
              (MNIST images are 28 x 28 = 784 so that is your default)
            hidden_dim: the inner dimension, a scalar
        '''
        print("======================================= Discriminator =========================================")
        total_image_pixels = np.prod(images_shape)
        num_layers = self.num_layers if self.num_layers else int(math.log(total_image_pixels, 2)) - int(math.log(hidden_dim, 2))
        print('layers', num_layers)

        model = keras.Sequential(name="discriminator")
        model.add(layers.InputLayer(input_shape=images_shape))

        model.add(layers.Flatten())
        for i in range(num_layers, 0, -1):
            model.add(layers.Dense(hidden_dim * i, name="discriminator_layer_" + str(i)))
            model.add(tf.keras.layers.LeakyReLU())
            model.add(layers.Dropout(0.3))

        model.add(layers.Dense(1))
        #model.add(layers.Activation('sigmoid'))
        self.optimizer.learning_rate = self.learning_rate
        print(model.summary())
        self.model = model


class Model():

    def __init__(self, learning_rate=None, optimizer=None, optimizer_keys=None, loss_function=None, loss_function_keys=None, metrics=None, metrics_keys=None,
                 code_length=8, num_generator_layers=-1, num_discriminator_layers=-1):

        self.generator = Generator(optimizer, learning_rate, num_layers=3)
        self.discriminator = Discriminator(optimizer, learning_rate)

        self.loss_function = loss_function
        self.metrics = metrics
        self.code_length = code_length

        self.loss_function_keys = loss_function_keys
        self.optimizer_keys = optimizer_keys
        self.metrics_keys = metrics_keys

    def build_model_graph(self, images_shape):
        print("images_shape:", images_shape)

        total_image_pixels = np.prod(images_shape)
        self.generator.build_graph(images_shape, self.code_length, hidden_dim=128)
        self.discriminator.build_graph(images_shape, hidden_dim=128)

    @tf.function
    def train_step(self, images, code_length, batch_size, eval=False):
        training = not eval
        def discriminator_loss(pred_real, pred_fake):
            real_loss = self.loss_function(tf.ones_like(pred_real), pred_real) # compares discriminator's predictions on real images to an array of 1s,
            fake_loss = self.loss_function(tf.zeros_like(pred_fake), pred_fake) # compares discriminator's predictions on fake (generated) images to an array of 0s.
            total_loss = (real_loss + fake_loss) / 2
            return total_loss

        def generator_loss(pred_fake):
            # Loss will be low is fake images have a higher score by discriminator of being 1, else viseversa
            return self.loss_function(tf.ones_like(pred_fake), pred_fake) # compares discriminators decisions on the generated images to an array of 1s.

        noise = tf.random.normal([batch_size, code_length])

        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:

            generated_images = self.generator.model(noise, training=training)

            pred_real = self.discriminator.model(images, training=training)
            pred_fake = self.discriminator.model(generated_images, training=training)

            gen_loss = generator_loss(pred_fake)
            disc_loss = discriminator_loss(pred_real, pred_fake)

        if training:
            gradients_of_generator = gen_tape.gradient(gen_loss, self.generator.model.trainable_variables)
            gradients_of_discriminator = disc_tape.gradient(disc_loss, self.discriminator.model.trainable_variables)

            self.generator.optimizer.apply_gradients(zip(gradients_of_generator, self.generator.model.trainable_variables))
            #if random.randint(1, 2) % 2 == 0:
            self.discriminator.optimizer.apply_gradients(zip(gradients_of_discriminator, self.discriminator.model.trainable_variables))
        return gen_loss, disc_loss

    def train(self, images_train, images_test, epochs=10, batch_size=16, validation_split=0.2):

        checkpoint = tf.train.Checkpoint(generator_optimizer=self.generator.optimizer, discriminator_optimizer=self.discriminator.optimizer,
                                         generator=self.generator.model,  discriminator=self.discriminator.model)

        # early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        print("================================= Training ===================================")

        generator = self.generator
        discriminator = self.discriminator
        code_length = self.code_length

        images_train, images_val = train_test_split(images_train, random_state=0, test_size=validation_split, shuffle=True)

        train_dataset = tf.data.Dataset.from_tensor_slices(images_train).shuffle(batch_size * 4).batch(batch_size)
        val_dataset = tf.data.Dataset.from_tensor_slices(images_val).shuffle(batch_size * 4).batch(batch_size)
        test_dataset = tf.data.Dataset.from_tensor_slices(images_test).shuffle(batch_size * 4).batch(batch_size)

        def _epoch(images, dataset, type, eval, epoch=None):
            total_generator_loss = 0
            total_discriminator_loss = 0
            steps = images.shape[0] / batch_size

            batch_log = tqdm(total=steps, position=0)

            for j, image_batch in enumerate(dataset):
                generator_loss, discriminator_loss = self.train_step(image_batch, code_length, batch_size, eval=eval)

                # Adjust weights only when training
                total_discriminator_loss += K.eval(discriminator_loss)
                total_generator_loss  += K.eval(generator_loss)

                mean_generator_loss = total_generator_loss / j
                mean_discriminator_loss = total_discriminator_loss / j

                batch_log.update(1)
                if epoch is not None:
                    batch_log.set_description(f'epoch: {i}, generator_loss({type}): {mean_generator_loss:10.8f}, discriminator_loss({type}): {mean_discriminator_loss: 10.8f}')
                else:
                    batch_log.set_description(f'generator_loss({type}): {mean_generator_loss:10.8f}, discriminator_loss({type}): {mean_discriminator_loss: 10.8f}')

        startime = datetime.now()
        for i in range(epochs):
            _epoch(images_train, train_dataset, "train", eval=False, epoch=i)
            _epoch(images_val, val_dataset, "val", eval=True, epoch=i)
            checkpoint.save(constants.DEFAULT_TF_CHECKPOINT)

        print("Total Training time:", datetime.now() - startime)

            # generator.fit(images_train, images_train, batch_size=batch_size, epochs=1, validation_split=validation_split,
            #       callbacks=[checkpoint, early_stopping], shuffle=True)
        #model.save(constants.DEFAULT_TF_MODELFILE) # Save Best model to disk

        print("================================= Evaluating ===================================")
        _epoch(images_val, val_dataset, "test", eval=True)

    def generate(self, n, codes=None, batch_size=8, print_model=False):
        """ This function is used to train model on given training images, based on data enoder part learns to compress images into intermediate dimension containing N points, and decoder learns to decipher the intermediate dimension. The indermediate dimention of N points (code_length), when randomly generated will produce new images.

        **Parameters**

        n: int
            number of images to be generated by our trained model
        codes: list
            Default: None, if passes then model will use this set of codes for generating images, else it will generate random distribution based on earlier calculated code statistics
        batch_size: int
            Default 16, batch_size used for training model.
        print_model: boolean
            Default False,  whether to print model information
        """
        print("================================= generating samples ===================================")
        if print_model:
            print(self.generator.model.summary())

        if codes is not None:
            inputs  = codes[:n]
        else:
            inputs = tf.random.normal([n, self.code_length])

        dataset = tf.data.Dataset.from_tensor_slices(inputs).shuffle(batch_size * 4).batch(batch_size)

        images_generated = []
        for i, noise_batch in enumerate(dataset):
            images_generated.append(self.generator.model(noise_batch, training=True))
        print(images_generated[0][0])
        images_generated = np.concatenate(images_generated)#.astype(np.uint8)
        #images_generated[images_generated > 255] = 255
        #images_generated[images_generated < 0] = 0
        return images_generated

    def save(self, modelfile):
        """ Function save model to a persistat storage

        **Parameters**

        modelfile: string
            Path where model needs to be saved
        """
        if not modelfile.endswith('.zip'):
            raise Exception('modelfile must ends with .zip as extention')

        if os.path.exists(modelfile):
            os.remove(modelfile)

        modelfile_cls = "tf_" + modelfile.split('.')[0] + ".pkl"
        modelfile_gen_tf = "tf_" + modelfile.split('.')[0] + "_gen.h5"
        modelfile_disc_tf = "tf_" + modelfile.split('.')[0] + "_disc.h5"

        self.generator.model.save(modelfile_gen_tf)
        self.discriminator.model.save(modelfile_disc_tf)

        generator = self.generator
        discriminator = self.discriminator

        metrics = self.metrics
        loss_function = self.loss_function

        self.discriminator.model = None
        self.discriminator.optimizer = None
        self.generator.model = None
        self.generator.optimizer = None
        self.metrics = None
        self.loss_function = None

        print("Pickle protocol:", pickle.HIGHEST_PROTOCOL)
        with open(modelfile_cls, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

        self.generator = generator
        self.discriminator = discriminator
        self.metrics = metrics
        self.loss_function = loss_function

        with ZipFile(modelfile, 'w') as zipobj:
           zipobj.write(modelfile_cls)
           zipobj.write(modelfile_gen_tf)
           zipobj.write(modelfile_disc_tf)

        os.remove(modelfile_cls)
        os.remove(modelfile_gen_tf)
        os.remove(modelfile_disc_tf)

        model_dir = constants.DEFAULT_TF_CHECKPOINT_DIR
        if os.path.exists(model_dir):
            print("Removing old model directory:", model_dir)
            shutil.rmtree(model_dir)
