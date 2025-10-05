import numpy as np


class SignalGenerator:

    def __init__(self):
        pass

    @staticmethod
    def sin_gen_s(f_hz: float, fd_hz: float, duration_s: float, amplitude: float = 0.9, phase: float = 0):
        t = np.linspace(0, duration_s, int(fd_hz * duration_s), endpoint=False)
        pixel_signal = amplitude * np.sin(2 * np.pi * f_hz * t + phase)
        return pixel_signal

    @staticmethod
    def sin_gen_samples(f_hz: float, fd_hz: float, samples_num: int, amplitude: float = 0.9, phase: float = 0):
        t = np.linspace(0, samples_num / fd_hz, samples_num, endpoint=False)
        pixel_signal = amplitude * np.sin(2 * np.pi * f_hz * t + phase)
        return pixel_signal
