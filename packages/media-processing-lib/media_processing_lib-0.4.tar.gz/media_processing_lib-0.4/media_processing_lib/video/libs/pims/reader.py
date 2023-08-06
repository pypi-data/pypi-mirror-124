import pims
import numpy as np
from typing import Tuple, List, Optional
from ....debug import Debug

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

def readRaw(path:str, nFrames:Optional[int]) -> ReadReturnType:
	Debug.log(1, "[mpl::video::pims] Reading raw data.")

	video = pims.Video(path)
	fps = video.frame_rate
	data = video
	if nFrames == None:
		nFrames = len(video)
	shape = (nFrames, *video.frame_shape)
	return data, fps, shape, nFrames