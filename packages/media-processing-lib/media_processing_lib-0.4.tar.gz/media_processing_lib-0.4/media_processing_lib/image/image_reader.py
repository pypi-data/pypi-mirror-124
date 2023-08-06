import numpy as np
from ..debug import Debug
from pathlib import Path

def tryReadImage(path:str, imgLib:str="opencv", count:int=5) -> np.ndarray:
	assert imgLib in ("opencv", "PIL", "pillow", "lycon")
	if imgLib == "opencv":
		from .libs.opencv import readImage
	elif imgLib in ("PIL", "pillow"):
		from .libs.pil import readImage
	elif imgLib == "lycon":
		from .libs.lycon import readImage

	path = str(path) if isinstance(path, Path) else path

	i = 0
	while True:
		try:
			return readImage(path)
		except Exception as e:
			Debug.log(1, "Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception(e)