import cv2
import numpy as np

def writeImage(file:np.ndarray, path:str):
	res = cv2.imwrite(path, file[..., ::-1])
	if not res:
		raise Exception("Image %s could not be saved to '%s'" % (file.shape, path))
