from src.utils.image_process import ImageProcess


class Robot8Bw:
    _max_res = (160, 120)
    _fd_hz = 44100
    _duration_per_px_s = 416.67e-6

    def __init__(self, filepath: str):
        self._im_proc = ImageProcess()
        self._filepath = filepath

    def code(self) -> bool:
        status = self._im_proc.im_open(self._filepath)
        if not status:
            return False

        self._im_proc.resolution_check(self._max_res)
        im_pixels = self._im_proc.pixels
        print(im_pixels)

    def decode(self):
        pass
