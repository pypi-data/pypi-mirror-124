import numpy as np
from ..debug import Debug

def tryWriteImage(file:np.ndarray, path:str, imgLib:str="opencv", count:int=5) -> None:
	path = str(path) if not isinstance(path, str) else path
	assert imgLib in ("opencv", "PIL", "pillow", "lycon")
	if imgLib == "opencv":
		from .libs.opencv import writeImage
	elif imgLib in ("PIL", "pillow"):
		from .libs.pil import writeImage
	elif imgLib == "lycon":
		from .libs.lycon import writeImage

	i = 0
	while True:
		try:
			return writeImage(file, path)
		except Exception as e:
			Debug.log(1, "Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception
