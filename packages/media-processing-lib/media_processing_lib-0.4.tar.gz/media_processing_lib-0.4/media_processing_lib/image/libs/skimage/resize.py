import numpy as np
from skimage.transform import resize

def resizeImage(data:np.ndarray, height:int, width:int, interpolation:str, **kwargs):
	assert interpolation in ("nearest", "bilinear", "bicubic", "biquadratic", "biquartic", "biquintic")
	assert isinstance(height, int) and isinstance(width, int)

	# As per: https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.warp
	order = {
		"nearest" : 0,
		"bilinear" : 1,
		"biquadratic" : 2,
		"bicubic" : 3,
		"biquartic" : 4,
		"biquintic" : 5
	}[interpolation]
	imgResized = resize(data, output_shape=(height, width), order=order, preserve_range=True, **kwargs)
	return imgResized.astype(data.dtype)
