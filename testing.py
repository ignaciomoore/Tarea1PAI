
import skimage.io as skio
import numpy as np
import math
from tarea_1 import encode_char_BW
from tarea_1 import decode_char_BW
from tarea_1 import encode_char_colour
'''
image = skio.io.imread('elephant.jpg')

def copy(image):
    new = image.copy()
    return new

new_image = copy(image)

new_image[0][0] = 5
'''

def encode(array, number):
    binNumber = bin(number)
    binNumber = binNumber[2:]
    binNumber = '0'*(8-len(binNumber))+binNumber
    print('Number to code: '+binNumber)

    for i in range(4):
        pixel = array[0][i]
        binPixel = bin(pixel)
        binPixel = binPixel[2:]
        binPixel = '0' * (8 - len(binPixel)) + binPixel

        for j in range(2):
            print('Before: '+binPixel)
            print((j+(i*2)))
            print(binNumber[j+(i*2)])
            binPixel = binPixel[:8-2+j] + binNumber[j+(i*2)] + binPixel[8-2+j+1:]
            print('After: '+binPixel)

        array[0][i] = int(binPixel,2)
        print(bin(array[0][i]))

    return array

arr = np.array([[244, 244, 248, 250],[233, 193, 191, 198],[233, 193, 191, 198],[233, 193, 191, 198]])



lion = skio.imread('lion_gray.jpg')

cat = lion.copy()

def decode_nbits(bits, array):
    binChar = ''
    pixels = math.ceil(8.0/bits)
    for i in range(pixels):
        pixel = array[0][i]
        binPixel = bin(pixel)
        binPixel = binPixel[2:]
        binPixel = '0' * (8 - len(binPixel)) + binPixel
        for j in range(bits):
            binChar += binPixel[8-bits+j]

    intChar = int(binChar,2)
    return intChar

def decode_char_BWTest(nBits, image, startI, startJ):

    pixels = math.ceil(8.0 / nBits)
    size = image.shape
    currentI = startI
    currentJ = startJ

    binCharacter = '' #binary version of the extracted character

    for j in range(pixels):

        if currentJ >= size[1]:
            currentI += 1
            currentJ = 0

        pixel = image[currentI][currentJ]

        binPixel = bin(pixel) #binary version of pixel
        binPixel = binPixel[2:]
        binPixel = '0' * (8 - len(binPixel)) + binPixel

        for k in range(nBits):
            if j+k+2 > 8:
                break
            binCharacter += binPixel[8-nBits+k]

        currentJ += 1

    Character = chr(int(binCharacter,2))
    return Character

copied_image = 'h'

def test_encode_BW_image(nBits, image, text):

    file = open(text,"r")
    str_text = file.read()
    new_image = image.copy()
    pixels = math.ceil(8.0/nBits)

    char_nBits = chr(nBits)

    current_line = 0
    current_column = 0

    #the nBits number is represented by 2 bits in each pixel
    #of the first 4 pixels
    encode_char_BW(2,new_image,current_line,current_column,char_nBits)

    current_column += 4

    size = new_image.shape

    encode_char_BW(nBits,new_image,current_line,current_column,chr(len(str_text)))

    if ((current_column + pixels) % size[1]) < current_column:
        current_line += 1

    current_column = (current_column + pixels) % size[1]

    for i in range(len(text)):

        encode_char_BW(nBits,new_image,current_line,current_column,text[i])

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

    for i in range(len(str_text)):

            encode_char_BW(nBits,new_image,current_line,current_column,str_text[i])

            new_column = (current_column+pixels)%size[1]

            if new_column < current_column:
                current_line += 1

            current_column = new_column

    return new_image

def test_decode_BW_image(image):

    char_nBits = decode_char_BW(2,image,0,0)
    print(char_nBits)
    nBits = ord(char_nBits)
    print(nBits)
    print(image[0][:4])
    pixels = math.ceil(8.0 / nBits)
    filename = ''
    current_line = 0
    current_column = 4
    size = image.shape

    content_size = ord(decode_char_BW(nBits,image,current_line,current_column))

    if ((current_column + pixels) % size[1]) < current_column:
        current_line += 1

    current_column = (current_column + pixels) % size[1]

    while filename.find('.txt') == -1:
        filename += decode_char_BW(nBits,image,current_line,current_column)

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

    index = filename.find('.')
    filename = filename[:index]+'_out'+filename[index:]
    file = open(filename,"w+")

    for i in range(len(content_size)):
        character = decode_char_BW(nBits,image,current_line,current_column)
        file.write(character)

        new_column = (current_column + pixels) % size[1]

        if new_column < current_column:
            current_line += 1

        current_column = new_column

'''
lion_in = skio.imread('lion_gray.jpg')

print('lion_in')
print(lion_in.shape)

c = decode_char_BWTest(2,lion_out,0,0)
print(c)
c = ord(c)
print(c)

print(lion_in[0][:4])
print('\nlion_out')
#print(lion_out.shape)
#print(lion_out[0][:4])
'''

def find_name(image):
    char_nBits = decode_char_BW(2, image, 0, 0)
    nBits = ord(char_nBits)
    print(nBits)
    pixels = math.ceil(8.0 / nBits)

    current_line = 0
    current_column = 4
    size = image.shape

    content_size = ord(decode_char_BW(nBits, image, current_line, current_column))
    print(content_size)

    if ((current_column + pixels) % size[1]) < current_column:
        current_line += 1

    current_column = (current_column + pixels) % size[1]

    a = (current_line, current_column)
    print(a)

    new = decode_char_BW(nBits,image,current_line,current_column)
    print(new)

    filename = ''
    while filename.find('.txt') != -1:
        filename += decode_char_BW(nBits,image,current_line,current_column)

        new_column = (current_column + 1)%size[1]
        if new_column<current_column:
            current_line+=1
        current_column = new_column

        if current_line >= size[0]:
            print('ran out of space')
            break

    print(filename)


original_image = skio.imread('flower_out.png')

print(original_image[0][:3])

#encode_char_colour(2,copied_image,0,0,'R')



'''
if copied_image.shape[0][0][0]:
    print('coloured')
'''
