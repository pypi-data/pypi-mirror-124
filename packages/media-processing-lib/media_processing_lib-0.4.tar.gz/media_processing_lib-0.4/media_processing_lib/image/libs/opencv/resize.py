import numpy as np
import cv2

def resizeImage(data:np.ndarray, height:int, width:int, interpolation:str, **kwargs):
	assert isinstance(height, int) and isinstance(width, int)

	# As per: https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
	interpolation = {
		"nearest" : cv2.INTER_NEAREST,
		"bilinear" : cv2.INTER_LINEAR,
		"area" : cv2.INTER_AREA,
		"bicubic" : cv2.INTER_CUBIC,
		"lanczos" : cv2.INTER_LANCZOS4
	}[interpolation]
	imgResized = cv2.resize(data, dsize=(width, height), interpolation=interpolation, **kwargs)
	return imgResized.astype(data.dtype)
