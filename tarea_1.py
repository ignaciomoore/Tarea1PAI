
import argparse

parser = argparse.ArgumentParser(description='Encode or Decode an Image')
parser.add_argument('--image', type=str, help='Image file name')
parser.add_argument('--text', type=str, help='Text file name')
parser.add_argument('--nbits', type=int, help='Cantidad de bits')
group = parser.add_mutually_exclusive_group()
group.add_argument('--encode', action='store_true', help='Encode text')
group.add_argument('--decode', action='store_true', help='Decode text')
args = parser.parse_args()

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