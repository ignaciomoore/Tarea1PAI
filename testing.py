
import skimage as skio
import numpy as np

image = skio.io.imread('elephant.jpg')

def copy(image):
    new = image.copy()
    return new

new_image = copy(image)

new_image[0][0] = 5

print(image[0][:20])
print(new_image[0][:20])
