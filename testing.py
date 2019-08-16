
import skimage.io as skio
import numpy as np
import math
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

b = 'h'


lion_in = skio.imread('lion_gray.jpg')

print('lion_in')
print(lion_in.shape)
'''
c = decode_char_BWTest(2,lion_out,0,0)
print(c)
c = ord(c)
print(c)
'''
print(lion_in[0][:4])
print('\nlion_out')
#print(lion_out.shape)
#print(lion_out[0][:4])
