import numpy as np
from PIL import Image

def resizeImage(data:np.ndarray, height:int, width:int, interpolation:str, **kwargs):
	assert data.dtype == np.uint8
	assert isinstance(height, int) and isinstance(width, int)
	imgData = Image.fromarray(data)

	# As per: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.resize
	resample = {
		"nearest" : Image.NEAREST,
		"bilinear" : Image.BILINEAR,
		"bicubic" : Image.BICUBIC,
		"lanczos" : Image.LANCZOS
	}[interpolation]

	imgResized = imgData.resize(size=(width, height), resample=resample, **kwargs)
	npImgResized = np.array(imgResized, dtype=data.dtype)
	return npImgResized
