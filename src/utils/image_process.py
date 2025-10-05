import numpy as np
from PIL import Image

from src.utils.m_types import ImResolution


class ImageProcess:

    def __init__(self):
        self._im: Image.Image = Image.Image()

    @property
    def pixels(self):
        return np.array(self._im)

    def im_show(self, pixels: np.array) -> None:
        im = Image.fromarray(pixels)
        im.show()

    def im_bw_convert(self) -> None:
        self._im = self._im.convert("L")

    def im_open(self, im_path: str) -> bool:
        try:
            self._im = Image.open(im_path)
        except FileNotFoundError as e:
            print(e)
            return False

        return True

    def resolution_check(self, max_res: ImResolution):
        if self._im.size > max_res:
            print(f"Image size {self._im.size} > max size {max_res}. Resizing")
            self._im = self._im.resize(max_res)

        print(f"Image Resolution {self._im.size}")


if __name__ == '__main__':
    im_proc = ImageProcess()
    status = im_proc.im_open(f'../../examples/test_samples/Test Pattern.jpg')
    im_proc.resolution_check((160, 120))
    px = im_proc.pixels
    print(px)
