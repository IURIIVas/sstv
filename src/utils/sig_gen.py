import numpy as np


class SignalGeneration:

    def __init__(self):
        pass

    @staticmethod
    def sin_gen(f_hz: float, fd_hz: float, duration_s: float, amplitude: float = 1):
        t = np.linspace(0, duration_s, int(fd_hz * duration_s), endpoint=False)
        pixel_signal = amplitude * np.sin(2 * np.pi * f_hz * t)
        return pixel_signal
