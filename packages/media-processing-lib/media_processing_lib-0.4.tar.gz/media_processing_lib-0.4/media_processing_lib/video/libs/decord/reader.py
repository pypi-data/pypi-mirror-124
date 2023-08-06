import numpy as np
from decord import VideoReader, cpu, gpu
from typing import Optional, List, Tuple
from pathlib import Path
from ....debug import Debug

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

def readRaw(path:Path, nFrames:Optional[int], context="cpu") -> ReadReturnType:
    Debug.log(2, "[mpl::video::decord] Reading raw data from '%s'" % path)
    context = {
        "cpu":cpu(0),
        "gpu":gpu(0)
    }[context]

    vr = VideoReader(str(path), ctx=context)
    nFrames = len(vr) if nFrames is None else nFrames
    shape = [nFrames, *vr[0].shape]
    fps = vr.get_avg_fps()
    return vr, fps, shape, nFrames
