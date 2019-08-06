
import argparse

parser = argparse.ArgumentParser(description='Encode or Decode an Image')
parser.add_argument('--image', type=str, help='Image file name')
group = parser.add_mutually_exclusive_group()
group.add_argument('--encode', action='store_true', help='Encode text')
group.add_argument('--decode', action='store_true', help='Decode text')
args = parser.parse_args()

if __name__ == '__main__':
    print(args.image)