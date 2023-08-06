import numpy as np
from typing import Callable
from ...debug import Debug

def imgResize_stretch(data:np.ndarray, height:int, width:int, interpolation:str, resizeFn:Callable, **kwargs):
	currentHeight, currentWidth = data.shape[0], data.shape[1]
	# If we provide width only, height is infered to keep image scale
	assert (height is None) + (width is None) < 2, "Both width and height cannot be infered. Provide at least one."
	if height is None:
		assert not width is None
		height = currentHeight / currentWidth * width
		if height != int(height):
			Debug.log(1, "[imgResize_stretch] Converting infered height from %2.2f to %d" % (heigt, int(height)))
		height = int(height)

	if width is None:
		assert not height is None
		width = currentWidth / currentHeight * height
		if width != int(width):
			Debug.log(1, "[imgResize_stretch] Converting infered width from %2.2f to %d" % (width, int(width)))
		width = int(width)

	return resizeFn(data, height, width, interpolation, **kwargs)
