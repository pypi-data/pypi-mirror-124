import cv2
import gimmick
import numpy as np

def load_images():
    # from sklearn import datasets
    # images = datasets.load_digits().images

    import numpy as np
    import tensorflow as tf
    (images, _), (_, _) = tf.keras.datasets.mnist.load_data()
    images = np.array([cv2.resize(x, (32, 32)) for x in images])
    return images


def train_model(modelfile, model_type, latent_dimension, num_encoder_layers, num_decoder_layers, optimizer, metrics,
                loss_function, epochs, batch_size, learning_rate, samples_for_code_statistics, images=None):

    print("Training data shape:", images.shape)

    if images is None:
        print("No Image dataset passes hence using Default images for training")
        images = load_images()

    print("Training started .......")
    """ Train and save model """
    model = gimmick.learn(images, algo=model_type, epochs=epochs, batch_size=batch_size, learning_rate=learning_rate,
                          metrics=[metrics], loss_function=loss_function, code_length=latent_dimension,
                          samples_for_code_statistics=samples_for_code_statistics,
                          num_encoder_layers=num_encoder_layers, num_decoder_layers=num_decoder_layers)
    model.save(modelfile)  # Saving model to be used later
    print("Training completed .......")


def get_model_details(modelfile):
    model = gimmick.load(modelfile) # loading model
    return {
        'code_stats': model.code_stats,
        'code_length': model.code_length
    }

def generate_image(model, code_values, random=False):
    print(model.code_stats)
    codes = [code_values] if not random else None
    images_gen = model.generate(1, batch_size=1, codes=codes) # Generate N random samples/images
    print(images_gen.shape)
    if images_gen[0].shape[-1] == 1:
        return cv2.cvtColor(images_gen[0], cv2.COLOR_GRAY2RGB)
    images_gen[0] = cv2.cvtColor(images_gen[0] , cv2.COLOR_BGR2RGB)
    return images_gen[0] #* 12

def generate_code(model, image):
    code = model.generate_code(np.array([image]))
    return code
