""" This module provide common utility function on images which are used across different sections
"""
import os
import cv2
import math
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

def convert_2dto3d(images):
    """ Function convert a list of 2D images to list of 3D images
    """

    print("convering images to 3d: shape before convert_2dto3d", images.shape)
    if len(images.shape) == 3:
        images = images.reshape(images.shape[0], images.shape[1], images.shape[2], 1)
    print("shape after convert_2dto3d", images.shape)
    return images

def plot_images(images, n_col=8, outputfile_path='img.png'):
    n_row = int(math.ceil(len(images) / n_col))
    fig = plt.figure(figsize=(6., 6.))

    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(n_row, n_col),  # creates 2x2 grid of axes
                 axes_pad=0.0,  # pad between axes in inch.
    )

    import cv2
    for ax, img in zip(grid, images):
        # Iterating over the grid returns the Axes.
        if type(img) == str and os.path.exists(img):
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             img = cv2.resize(img, (64, 64))  # Reshaping for visualization

        if len(img.shape) == 3 and img.shape[2] == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        ax.imshow(img)
    plt.show()

    colored_image  = outputfile_path

    gray_image  = 'gray_' + outputfile_path
    plt.savefig(colored_image)
    Image.open(colored_image).convert('L').save(gray_image)
    return colored_image, gray_image

def read_images_from_disk(trainig_files):
    images = [cv2.imread(x) for x in trainig_files]
    images = np.array(images)
    return images

def rescale_images(images, img_width, img_height, img_channels):
    images = [cv2.resize(x, (img_width, img_height)) for x in images]  # Reshaping for visualization
    images = np.array(images)
    return images

if __name__ == "__main__":
    from sklearn import datasets
    digits = datasets.load_digits()
    images = digits.images  # It contains roughly 1800 images of shape 8 x 8
    print("shape before convert_2dto3d", images.shape)
    images = convert_2dto3d(images)
    print("shape after convert_2dto3d", images.shape)
