
import skimage as skio
import numpy as np

image = skio.io.imread('elephant.jpg')

new_image = image.copy()

new_image[0][0] = 0

size = image.shape



