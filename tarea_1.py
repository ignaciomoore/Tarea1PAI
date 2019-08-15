
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
'''

def encode_char_BW(nBits, image, startI, startJ, char):

    pixels = math.ceil(8.0 / nBits)
    size = image.shape
    currentI = startI
    currentJ = startJ

    binaryC = bin(ord(char))
    binaryC = binaryC[2:]
    binaryC = '0'*(8-len(binaryC))+binaryC


    for j in range(pixels):

        if currentJ >= size[1]:
            currentI += 1
            currentJ = 0

        if currentI >= size[0]:
            return print('Not enough space in the image')

        pixel = image[currentI][currentJ]

        binaryP = bin(pixel)
        binaryP = binaryP[2:]
        binaryP = '0' * (8 - len(binaryP)) + binaryP

        new_pixel = binaryP[:len(binaryP)-nBits]
        new_bits = ''

        for k in range(nBits):
            if j+k+2 > 8:
                break
            new_bits += binaryC[j*2+k]

        new_pixel += new_bits
        new_colour = int(new_pixel,2)
        image[currentI][currentJ] = new_colour

        currentJ += 1

def encode_BW_image(nBits, image, text):

    file = open(text,"r")
    new_image = image.copy()
    pixels = math.ceil(8/nBits)

    binBits = bin(nBits)
    binBits = binBits[2:]
    binBits = '0'*(8-len(binBits))+binBits
    binBits = chr(int(binBits))

    current_line = 0
    current_column = 0

    #the nBits number es represented by 2 bits in each pixel
    #of the first 4 pixels
    encode_char_BW(2,new_image,current_line,current_column,binBits)

    current_column += 4

    size = new_image.shape

    while current_line < size[0]:
        while current_column < size[1]:

            char = file.read(1)
            if char == '':
                print('all done!')
                return new_image

            encode_char_BW(nBits,new_image,current_line,current_column,char)

            new_column = (current_column+pixels)%size[1]

            if new_column < current_column:
                current_line += 1

            current_column = new_column

    return new_image

if __name__ == '__main__':
    image = args.image
    print(image)
    if args.encode:
        print('Encoding')
        bits = args.nbits
        text = args.text

        picture = skio.imread(image)
        print(picture[0][:20])
        new_image = encode_BW_image(bits,picture,text)
        print(new_image[0][:20])

    elif args.decode:
        print('Decoding')
    else:
        print('Somethings wrong')

'''
    plt.imshow(picture, cmap='gray')
    plt.title(image)
    plt.axis('off')
    plt.show()
'''