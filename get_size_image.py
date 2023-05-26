import argparse

import cv2


def main(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    print(f"Height: {height}, Width: {width}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get image dimensions.')
    parser.add_argument('image_path', metavar='image_path', type=str, help='path to the image file')
    args = parser.parse_args()
    main(args.image_path)
