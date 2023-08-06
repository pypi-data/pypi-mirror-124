import numpy as np
from lycon import resize as resizeFn, Interpolation

# @brief Lycon based image resizing function
# @param[in] height Desired resulting height
# @param[in] width Desired resulting width
# @param[in] interpolation method. Valid options: bilinear, nearest, cubic, lanczos, area
# @return Resized image.
def resizeImage(data:np.ndarray, height:int, width:int, interpolation:str, **kwargs):
	assert interpolation in ("bilinear", "nearest", "bicubic", "lancsoz", "area")
	assert isinstance(height, int) and isinstance(width, int)

	# As per: https://github.com/ethereon/lycon/blob/046e9fab906b3d3d29bbbd3676b232bd0bc82787/perf/benchmark.py#L57
	interpolationTypes = {
		"bilinear" : Interpolation.LINEAR,
		"nearest" : Interpolation.NEAREST,
		"bicubic" : Interpolation.CUBIC,
		"lanczos" : Interpolation.LANCZOS,
		"area" : Interpolation.AREA
	}

	interpolationType = interpolationTypes[interpolation]
	imgResized = resizeFn(data, height=height, width=width, interpolation=interpolationType, **kwargs)
	return imgResized.astype(data.dtype)
