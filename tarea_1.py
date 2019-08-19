
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

#Black and White
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

    '''encode the nBits number with 2 bits in each pixel of the first 4 pixels'''
    encode_char_BW(2, new_image, current_line, current_column, char_nBits)

    current_column += 4

    size = new_image.shape

    '''encode the number of the length of the text'''
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

#Coloured
'''
Encodes char into the image, starting from de pixel image[startI][startJ][startW].
Also returns the location of the next available pixel'''
def encode_char_colour(nBits, image, startI, startJ, startW, char):

    number_pixels = math.ceil(8.0 / nBits)
    size = image.shape
    current_I = startI
    current_J = startJ
    current_W = startW

    binary_character = bin(ord(char))
    binary_character = binary_character[2:]
    binary_character = '0' * (8 - len(binary_character)) + binary_character

    for j in range(number_pixels):

        if current_W >= size[2]:
            current_J += 1
            current_W = 0

        if current_J >= size[1]:
            current_I += 1
            current_J = 0

        if current_I >= size[0]:
            return print('Not enough space in the image')

        pixel = image[current_I][current_J][current_W]
        binary_pixel = bin(pixel)
        binary_pixel = binary_pixel[2:]
        binary_pixel = '0' * (8 - len(binary_pixel)) + binary_pixel

        for k in range(nBits):
            if (j * nBits) + k >= 8:
                break

            binary_pixel = binary_pixel[:8 - nBits + k] + binary_character[k + (j * nBits)] + binary_pixel[
                                                                                              8 - nBits + k + 1:]

        image[current_I][current_J][current_W] = int(binary_pixel, 2)

        current_W += 1

    next_pixel = (current_I, current_J, current_W)
    return next_pixel

'''Encodes de text into a copy of the image and returns it.'''
def encode_coloured_image(nBits, image, text):
    file = open(text, "r")
    str_text = file.read()
    new_image = image.copy()
    pixels = math.ceil(8.0 / nBits)

    char_nBits = chr(nBits)

    current_I = 0
    current_J = 0
    current_W = 0

    '''Encodes the nBits number with an nbits equal to 3 bits'''
    encode_char_colour(3, new_image, current_I, current_J, current_W, char_nBits)

    current_J += 1

    size = new_image.shape

    '''Encodes the size of the text'''
    encode_char_colour(nBits, new_image, current_I, current_J, current_W, chr(len(str_text)))

    if ((current_W + pixels) % size[2]) < current_W:
        if ((current_J + 1) % size[1]) < current_J:
            current_I += 1
        current_J = (current_J + 1) % size[1]
    current_W = (current_W + pixels) % size[2]

    '''Encodes the name of the text file'''
    for i in range(len(text)):

        encode_char_colour(nBits, new_image, current_I, current_J, current_W, text[i])

        new_W = (current_W + pixels) % size[2]

        if new_W < current_J:
            new_J = current_J + 1
            if new_J % size[1] < current_J:
                current_I += 1
            current_J = new_J
        current_W = new_W

    '''Encodes the content of the text'''
    for i in range(len(str_text)):

        encode_char_colour(nBits, new_image, current_I, current_J, current_W, str_text[i])

        new_W = (current_W + pixels) % size[2]

        if new_W < current_J:
            new_J = current_J + 1
            if new_J % size[1] < current_J:
                current_I += 1
            current_J = new_J
        current_W = new_W

    return new_image

'''
Returns the next character in the image, starting from the position image[startI][startJ].'''
def decode_char_colour(nBits, image, startI, startJ, startW):

    number_of_pixels = math.ceil(8.0 / nBits)
    size = image.shape
    current_I = startI
    current_J = startJ
    current_W = startW

    binary_character = ''  # binary version of the extracted character

    for j in range(number_of_pixels):

        if current_W >= size[2]:
            current_J += 1
            current_W = 0

        if current_J >= size[1]:
            current_I += 1
            current_J = 0

        if current_I >= size[0]:
            return print('Ran out of space')

        pixel = image[current_I][current_J][current_W]
        binary_pixel = bin(pixel)  # binary version of pixel
        binary_pixel = binary_pixel[2:]
        binary_pixel = '0' * (8 - len(binary_pixel)) + binary_pixel

        for k in range(nBits):
            if 8 - nBits + k >= 8:
                break
            binary_character += binary_pixel[8 - nBits + k]

        current_W += 1

    binary_character = binary_character[:8]
    character = chr(int(binary_character, 2))
    return character

def decode_coloured_image(image):

    '''Decoding the value of nBits'''
    char_nBits = decode_char_colour(3, image, 0, 0, 0)
    nBits = ord(char_nBits)
    print(nBits)
    pixels = math.ceil(8.0 / nBits)
    filename = ''
    current_I = 0
    current_J = 1
    current_W = 0
    size = image.shape

    '''decoding size of content'''
    content_size = ord(decode_char_colour(nBits, image, current_I, current_J, current_W))
    print(content_size)
    if ((current_W + pixels) % size[2]) < current_W:
        if ((current_J + 1) % size[1]) < current_J:
            current_I += 1
        current_J = (current_J + 1) % size[1]
    current_W = (current_W + pixels) % size[2]

    a = (current_I,current_J,current_W)
    print(a)

    '''Decoding the name of the text file'''
    while filename.find('.txt') == -1:
        filename += decode_char_colour(nBits, image, current_I, current_J, current_W)

        new_W = (current_W + pixels) % size[2]

        if new_W < current_J:
            new_J = current_J + 1
            if new_J % size[1] < current_J:
                current_I += 1
            current_J = new_J
        current_W = new_W

    index = filename.find('.')
    filename = filename[:index] + '_out' + filename[index:]
    file = open(filename, "w+")

    for i in range(content_size):
        character = decode_char_BW(nBits, image, current_I, current_J, current_W)
        file.write(character)

        new_W = (current_W + pixels) % size[2]

        if new_W < current_J:
            new_J = current_J + 1
            if new_J % size[1] < current_J:
                current_I += 1
            current_J = new_J
        current_W = new_W

if __name__ == '__main__':
    image = args.image
    picture = skio.imread(image)
    size = picture.shape

    if args.encode:
        print('Encoding')
        print(image)
        bits = args.nbits
        text = args.text

        new_image = 0

        if len(size) == 2:
            new_image = encode_BW_image(bits,picture,text)
        elif len(size) == 3:
            new_image = encode_coloured_image(bits,picture,text)

        index = image.find('.')
        filename = image[:index]+'_out.png'
        skio.imsave(filename,new_image)

    elif args.decode:
        print('Decoding')
        print(image)

        if len(size) == 2:
            decode_BW_image(picture)
        elif len(size) == 3:
            decode_coloured_image(picture)

    else:
        print('Somethings wrong')

'''
    plt.imshow(picture, cmap='gray')
    plt.title(image)
    plt.axis('off')
    plt.show()
'''