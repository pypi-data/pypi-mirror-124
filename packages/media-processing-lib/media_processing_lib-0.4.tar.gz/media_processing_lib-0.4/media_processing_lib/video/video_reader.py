import numpy as np
import ffmpeg
from pathlib import Path
from typing import Optional

from .mpl_video import MPLVideo
from ..debug import Debug

def isRotated90(path, data, shape):
	ix = []
	f = ffmpeg.probe(path)
	for i, stream in enumerate(f["streams"]):
		if ("codec_type" in stream) and (stream["codec_type"] == "video"):
			ix.append(i)
	assert len(ix) == 1
	stream = f["streams"][ix[0]]

	# Other weird cases ? We'll see...
	if (not "tags" in stream) or (not "rotate" in stream["tags"]):
		return False

	if stream["tags"]["rotate"] != "90":
		return False

	# Some good shit happening here.
	strType = str(type(data)).split(".")[-1][0:-2]
	# Basically, ImageIOReader decided to transpose it by default for us.
	if strType == "ImageIOReader":
		return False
	# PyAVTimedReader decided to not transpose it at all.
	elif strType == "PyAVReaderTimed":
		return True
	# We'll see for other cases... we assume to it is not transposed.
	return True

def tryReadVideo(path:str, vidLib:str="imageio", count:int=5, nFrames:Optional[int]=None, **kwargs) -> MPLVideo:
	path = Path(path).resolve()
	extension = path.suffix.lower()[1 :]
	assert extension in ("gif", "mp4", "mov", "mkv")
	assert vidLib in ("imageio", "pims", "opencv", "decord")

	if vidLib == "pims":
		from .libs.pims import readRaw as readFn
	elif vidLib == "imageio":
		from .libs.imageio import readRaw as readFn
	elif vidLib == "opencv":
		from .libs.opencv import readRaw as readFn
	elif vidLib == "decord":
		from .libs.decord import readRaw as readFn

	i = 0
	while True:
		try:
			data, fps, shape, nFrames = readFn(path, nFrames, **kwargs)
			isPortrait = isRotated90(path, data, shape)
			assert len(shape) == 4
			video = MPLVideo(data, fps, isPortrait, shape, nFrames)
			Debug.log(1, "[mpl::tryReadVideo] Read video %s. Shape: %s. FPS: %2.3f. Portrait: %s. Video library: %s" \
				% (path, str(video.shape), video.fps, isPortrait, vidLib))
			return video
		except Exception as e:
			Debug.log(1, "[mpl::tryReadVideo] Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception(e)
