import cv2

def __main__():
    image = cv2.imread("image.png")
    height = image.shape[0]
    width = image.shape[1]
    print(height, width)

__main__()