
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
int -> binary: bin(int)
binary -> int: int(binary,2)
char -> int: ord(char)
int -> char: chr(int)'''

'''Encodes char into the image, starting from de pixel image[startI][startJ].
Also returns the location of the next available pixel'''
def encode_char_BW(nBits, image, startI, startJ, char):

    number_pixels = math.ceil(8.0 / nBits)
    size = image.shape
    current_line = startI
    current_column = startJ

    binary_character = bin(ord(char))
    binary_character = binary_character[2:]
    binary_character = '0'*(8-len(binary_character))+binary_character

    for j in range(number_pixels):

        if current_column >= size[1]:
            current_line += 1
            current_column = 0

        if current_line >= size[0]:
            return print('Not enough space in the image')

        pixel = image[current_line][current_column]
        binary_pixel = bin(pixel)
        binary_pixel = binary_pixel[2:]
        binary_pixel = '0' * (8 - len(binary_pixel)) + binary_pixel

        for k in range(nBits):
            if (j*nBits)+k >= 8:
                break

            binary_pixel = binary_pixel[:8-nBits+k] + binary_character[k+(j*nBits)] + binary_pixel[8-nBits+k+1:]


        image[current_line][current_column] = int(binary_pixel,2)

        current_column += 1

    next_pixel = (current_line,current_column)
    return next_pixel

'''Encodes de text into a copy of the image and returns it.'''
def encode_BW_image(nBits, image, text):
    file = open(text, "r")
    str_text = file.read()
    new_image = image.copy()
    pixels = math.ceil(8.0 / nBits)

    char_nBits = chr(nBits)

    current_line = 0
    current_column = 0

    # the nBits number is represented by 2 bits in each pixel
    # of the first 4 pixels
    encode_char_BW(2, new_image, current_line, current_column, char_nBits)

    current_column += 4

    size = new_image.shape

    encode_char_BW(nBits, new_image, current_line, current_column, chr(len(str_text)))

    if ((current_column + pixels) % size[1]) < current_column:
        current_line += 1

    current_column = (current_column + pixels) % size[1]

    for i in range(len(text)):

        encode_char_BW(nBits, new_image, current_line, current_column, text[i])

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

    for i in range(len(str_text)):

        encode_char_BW(nBits, new_image, current_line, current_column, str_text[i])

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

    return new_image

'''
Returns the next character in the image, starting from the position image[startI][startJ].'''
def decode_char_BW(nBits, image, startI, startJ):

    number_of_pixels = math.ceil(8.0 / nBits)
    size = image.shape
    current_line = startI
    current_column = startJ

    binary_character = ''   #binary version of the extracted character

    for j in range(number_of_pixels):

        if current_column >= size[1]:
            current_line += 1
            current_column = 0

        if current_line >= size[0]:
            return print('Ran out of space')

        pixel = image[current_line][current_column]
        binary_pixel = bin(pixel)   #binary version of pixel
        binary_pixel = binary_pixel[2:]
        binary_pixel = '0' * (8 - len(binary_pixel)) + binary_pixel

        for k in range(nBits):
            if 8-nBits+k >= 8:
                break
            binary_character += binary_pixel[8-nBits+k]

        current_column += 1

    binary_character = binary_character[:8]
    character = chr(int(binary_character, 2))
    return character

'''Decodes the image and creates a text file with the encoded text'''
def decode_BW_image(image):
    char_nBits = decode_char_BW(2, image, 0, 0)
    nBits = ord(char_nBits)
    pixels = math.ceil(8.0 / nBits)
    filename = ''
    current_line = 0
    current_column = 4
    size = image.shape

    content_size = ord(decode_char_BW(nBits, image, current_line, current_column))

    if ((current_column + pixels) % size[1]) < current_column:
        current_line += 1

    current_column = (current_column + pixels) % size[1]

    a = (current_line, current_column)

    while filename.find('.txt') == -1:
        filename += decode_char_BW(nBits, image, current_line, current_column)

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

    index = filename.find('.')
    filename = filename[:index] + '_out' + filename[index:]
    file = open(filename, "w+")

    for i in range(content_size):
        character = decode_char_BW(nBits, image, current_line, current_column)
        file.write(character)

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

def encode_char_colour(nBits, image, startI, startJ,char):

if __name__ == '__main__':
    image = args.image

    if args.encode:
        print('Encoding')
        print(image)
        bits = args.nbits
        text = args.text

        picture = skio.imread(image)
        new_image = encode_BW_image(bits,picture,text)

        index = image.find('.')
        filename = image[:index]+'_out.png'
        skio.imsave(filename,new_image)

    elif args.decode:
        print('Decoding')
        print(image)
        picture = skio.imread(image)
        decode_BW_image(picture)

    else:
        print('Somethings wrong')

'''
    plt.imshow(picture, cmap='gray')
    plt.title(image)
    plt.axis('off')
    plt.show()
'''