import cv2
import numpy as np

def readImage(path:str):
	bgr_image = cv2.imread(path)[..., 0 : 3]
	b, g, r = cv2.split(bgr_image)
	image = cv2.merge([r, g, b]).astype(np.uint8)
	return image
