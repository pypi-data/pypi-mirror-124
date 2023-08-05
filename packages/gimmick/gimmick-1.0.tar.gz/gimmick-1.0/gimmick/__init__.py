import os
import pickle
import tensorflow as tf
from gimmick.distributer import *
from gimmick import mapping
from zipfile import ZipFile

def load(modelfile):
    modelfile_cls = "tf_" + modelfile.split('.')[0] + ".pkl"

    with ZipFile(modelfile, 'r') as zip:
        zip.printdir()
        zip.extractall()

    modelobj = pickle.load(open(modelfile_cls, 'rb'))

    def _load_gans():
        modelfile_tf = "tf_" + modelfile.split('.')[0] + ".h5"
        modelfile_gen_tf = "tf_" + modelfile.split('.')[0] + "_gen.h5"
        modelfile_disc_tf = "tf_" + modelfile.split('.')[0] + "_disc.h5"

        modelobj.generator.model = tf.keras.models.load_model(modelfile_gen_tf)
        modelobj.discriminator.model = tf.keras.models.load_model(modelfile_disc_tf)

        os.remove(modelfile_cls)
        os.remove(modelfile_gen_tf)

        modelobj.metrics = [mapping.metrics_mapping.get(x) for x in modelobj.metrics_keys]
        modelobj.loss_function = mapping.loss_function_mapping.get(modelobj.loss_function_keys)
        modelobj.generator.optimizer = mapping.optimizer_mapping.get(modelobj.optimizer_keys)
        modelobj.discriminator.optimizer = mapping.optimizer_mapping.get(modelobj.optimizer_keys)

        return modelobj

    def _load_autoencoders():
        modelfile_tf = "tf_" + modelfile.split('.')[0] + ".h5"
        modelfile_ig_tf = "tf_" + modelfile.split('.')[0] + "_ig.h5"
        modelfile_cg_tf = "tf_" + modelfile.split('.')[0] + "_cg.h5"

        modelobj.model = tf.keras.models.load_model(modelfile_tf)
        modelobj.model_image_generator = tf.keras.models.load_model(modelfile_ig_tf)
        modelobj.model_code_generator = tf.keras.models.load_model(modelfile_cg_tf)
        os.remove(modelfile_ig_tf)
        os.remove(modelfile_cg_tf)
        os.remove(modelfile_cls)
        os.remove(modelfile_tf)

        modelobj.metrics = [mapping.metrics_mapping.get(x) for x in modelobj.metrics_keys]
        modelobj.optimizer = mapping.optimizer_mapping.get(modelobj.optimizer_keys)
        modelobj.loss_function = mapping.loss_function_mapping.get(modelobj.loss_function_keys)
        return modelobj

    if ".gan" in str(modelobj):
        return _load_gans()
    return _load_autoencoders()
