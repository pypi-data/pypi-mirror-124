import numpy as np
import lycon

def readImage(path:str):
	image = lycon.load(path)[..., 0 : 3].astype(np.uint8)
	return image
