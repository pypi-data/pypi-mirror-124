import numpy as np
from PIL import Image

def readImage(path:str):
	image = np.array(Image.open(path), dtype=np.uint8)[..., 0 : 3]
	return image
