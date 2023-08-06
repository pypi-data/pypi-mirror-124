import numpy as np
from PIL import Image

def writeImage(file:np.ndarray, path:str):
	assert file.min() >= 0 and file.max() <= 255
	img = Image.fromarray(file.astype(np.uint8), "RGB")
	img.save(path)
