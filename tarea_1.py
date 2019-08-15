
import argparse
import skimage.io as skio
import numpy as np
import matplotlib.pyplot as plt
import math

parser = argparse.ArgumentParser(description='Encode or Decode an Image')
parser.add_argument('--image', type=str, help='Image file name')
parser.add_argument('--text', type=str, help='Text file name')
parser.add_argument('--nbits', type=int, help='Cantidad de bits')
group = parser.add_mutually_exclusive_group()
group.add_argument('--encode', action='store_true', help='Encode text')
group.add_argument('--decode', action='store_true', help='Decode text')
args = parser.parse_args()
'''
def to_uint8(image) :
    if image.dtype == np.float64 :
        image = image * 255
    image[image<0]=0
    image[image>255]=255
    image = image.astype(np.uint8, copy=False)
    return image

def imread(filename, as_gray = False):
    image = skio.imread(filename, as_gray = as_gray)
    if image.dtype == np.float64:
        image = to_uint8(image)
    return image
'''

def change_BW_Bits(nBits, image, startI, startJ, char):

    pixels = math.ceil(8.0/nBits)
    size = image.shape
    currentI = startI
    currentJ = startJ

    for j in range(pixels):

        mask = ord(char)
        mask >>= (2*j)
        mask &= ~(-1 << nBits) #bits que se deben ingresar

        if j+startJ >= size[1]:
            currentJ = 0
            currentI += 1

        if currentI >= size[0]:
            return print('Not enough space')
#IM STUCK, CANT CHANGE THE BITS
        for b in range(nBits):
            mask
            image[currentI][currentJ] = image[currentI][currentJ]


if __name__ == '__main__':
    image = args.image
    if args.encode:
        print('Encoding')
        bits = args.nbits
        text = args.text
        print(text)
        print(bits)
    elif args.decode:
        print('Decoding')
    else:
        print('Somethings wrong')
    print(image)

    picture = skio.imread(image)
    print('shape: {}'.format(picture.shape))

    print(picture)

'''
    plt.imshow(picture, cmap='gray')
    plt.title(image)
    plt.axis('off')
    plt.show()
'''