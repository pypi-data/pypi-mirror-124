import numpy as np
from pathlib import Path
from typing import List, Optional, Callable
from tqdm import trange
from natsort import natsorted
from media_processing_lib.image import tryWriteImage
from PIL import Image, ImageFont, ImageDraw, ImageOps

# @brief Make a concatenated collage based on the desired r,c format
def collageFn(images:List[np.ndarray], rows:int, cols:int, titles:Optional[List[str]]=None) -> np.ndarray:
    imageShape = images[0].shape
    height, width = imageShape[0 : 2]

    if titles is not None:
        images = [Image.fromarray(x) for x in images]
        # Left, Top, Right, Bottom
        border = (0, int(height * 0.15), int(width * 0.02), 0)
        font = ImageFont.truetype("OpenSans-Bold.ttf", int(border[1] * 1))
        images = [ImageOps.expand(x, border=border, fill=(0, 0, 0)) for x in images]
        for image, title in zip(images, titles):
            draw = ImageDraw.Draw(image)
            w, h = draw.textsize(title, font)
            draw.text(((width - w) / 2, -border[1] / 5), title, fill="white", font=font)
        images = [np.array(x) for x in images]
        imageShape = images[0].shape
    
    result = np.zeros((rows * cols, *imageShape), dtype=np.uint8)
    result[0 : len(images)] = np.array(images)
    result = result.reshape((rows, cols, *imageShape))
    result = np.concatenate(np.concatenate(result, axis=1), axis=1)
    return result

class CollageMaker:
    def __init__(self, dirs:List[Path], plotFns:List[Callable], outputDir:Path, names:Optional[List[str]]=None):
        assert len(dirs) > 0
        self.dirs = list(dirs)
        self.plotFns = plotFns
        self.outputDir = outputDir
        self.names = names if not names is None else len(self.dirs) * [""]
        assert len(self.dirs) == len(self.plotFns) == len(self.names)

        self.files = self.getFiles()
        self.rowCols = CollageMaker.getSquareRowsColumns(len(self.dirs))

    def getFiles(self) -> List[List[str]]:
        res = []
        for dir in self.dirs:
            files = natsorted([str(x) for x in dir.glob("*.npz")])
            assert len(files) > 0
            res.append(files)
        assert np.std([len(x) for x in res]) == 0
        # Min = min([len(x) for x in res])
        # res = [x[0:Min] for x in res]
        res = np.array(res)
        return res

    @staticmethod
    def getSquareRowsColumns(N):
        x = int(np.sqrt(N))
        r, c = x, x
        # There are only 2 rows possible between x^2 and (x+1)^2 because (x+1)^2 = x^2 + 2*x + 1, thus we can add 2 columns
        #  at most. If a 3rd column is needed, then closest lower bound is (x+1)^2 and we must use that.
        if c * r < N:
            c += 1
        if c * r < N:
            r += 1
        assert (c + 1) * r > N and c * (r + 1) > N
        return r, c

    # Given a stack of N images, find the closest square X>=N*N and then remove rows 1 by 1 until it still fits X
    # Example: 9: 3*3; 12 -> 3*3 -> 3*4 (3 rows). 65 -> 8*8 -> 8*9. 73 -> 8*8 -> 8*9 -> 9*9
    def makeCollage(self, startIx:Optional[int]=None, endIx:Optional[int]=None) -> np.ndarray:
        from ..image_writer import tryWriteImage

        startIx = startIx if not startIx is None else 0
        endIx = endIx if not endIx is None else len(self.files[0])
        assert startIx < endIx
        assert endIx <= len(self.files[0]), "%d vs %d" % (endIx, len(self.files[0]))
        self.outputDir.mkdir(parents=True, exist_ok=False)
        open(self.outputDir / "order.txt", "w").write(",".join(self.names))

        def loadFn(x):
            try:
                return np.load(x)["arr_0"]
            except:
                return np.load(x, allow_pickle=True)["arr_0"].item()["data"]

        for i in trange(startIx, endIx):
            thisPaths = self.files[:, i]
            items = [loadFn(x) for x in thisPaths]
            images = [self.plotFns[j](items[j]) for j in range(len(items))]
            result = collageFn(images, self.rowCols[0], self.rowCols[1], self.names)
        
            # Save to disk
            outFile = f"{self.outputDir}/{i}.png"
            tryWriteImage(result, outFile)
