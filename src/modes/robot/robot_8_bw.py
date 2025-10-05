from scipy.io import wavfile
import numpy as np

from src.utils.image_process import ImageProcess
from src.utils.sig_gen import SignalGenerator
from src.utils.signal_plot import plot_build


_possible_fd = [8000, 11025, 12000, 14000, 16000, 18000, 22050, 24000, 44100, 48000]


class Robot8Bw:
    _max_res = (160, 120)

    # horizontal sync
    _sync_freq_hz = 1200
    _porch_freq_hz = 1500

    # pixels
    _black_px_freq_hz = 1500
    _white_px_freq_hz = 2300

    # vis
    _l_tone_freq_hz = 1900
    _zero_bit_freq_hz = 1300
    _one_bit_freq_hz = 1100
    _start_bit_freq_hz = 1200
    _stop_bit_freq_hz = 1200

    # constant duration s
    _line_duration_s = 66.9e-3
    _l_tone_duration_s = 0.3
    _l_tone_pause_duration_s = 10e-3
    _vis_code_bits_duration_s = 30e-3
    _v_sync_duration_s = 10e-3
    _h_sync_duration_s = 5.4e-3
    _porch_duration_s = 1.5e-3

    def __init__(self, filepath: str, sample_rate_hz: int):
        if sample_rate_hz not in _possible_fd:
            print("Incorrect ")
        self._sample_rate_hz = sample_rate_hz
        self._sample_duration_s = 1 / sample_rate_hz

        self._im_proc = ImageProcess()
        self._filepath = filepath
        self._signal_gen = SignalGenerator()

    def _px_freq_hz_get(self, px: int) -> float:
        freq_step_hz = (self._white_px_freq_hz - self._black_px_freq_hz) / 256
        return self._black_px_freq_hz + (px * freq_step_hz)

    def _sync_insert(self, pixels_freq_hz: np.array) -> np.array:
        # vis code bits for robot 8bw: b1(p)0000001, p - parity = 1
        header = [
            self._l_tone_freq_hz,
            self._sync_freq_hz,
            self._l_tone_freq_hz,
            self._start_bit_freq_hz,
            self._zero_bit_freq_hz,
            self._one_bit_freq_hz,
            self._zero_bit_freq_hz,
            self._zero_bit_freq_hz,
            self._zero_bit_freq_hz,
            self._zero_bit_freq_hz,
            self._zero_bit_freq_hz,
            self._one_bit_freq_hz,  # parity
            self._stop_bit_freq_hz,
            self._sync_freq_hz
        ]
        pixels_freq_hz = pixels_freq_hz.reshape((120, 160))

        structured_lines = []
        for i in range(120):

            line_frequencies = [
                self._sync_freq_hz,
                self._porch_freq_hz,
                *pixels_freq_hz[i]
            ]
            structured_lines.extend(line_frequencies)

        pixels_freq_hz = np.concatenate((np.array(header), np.array(structured_lines)))
        return pixels_freq_hz

    def _durations_get(self) -> np.array:
        header_durations_s = [
            self._l_tone_duration_s,
            self._l_tone_pause_duration_s,
            self._l_tone_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._vis_code_bits_duration_s,
            self._v_sync_duration_s
        ]
        header_durations_samples = [int(dur_s / self._sample_duration_s) for dur_s in header_durations_s]

        line_samples = int(self._line_duration_s / self._sample_duration_s)
        h_sync_samples = int(self._h_sync_duration_s / self._sample_duration_s)
        front_porch_samples = int(np.floor(self._porch_duration_s / self._sample_duration_s))
        line_active_pixels_samples = line_samples - h_sync_samples - front_porch_samples

        components_per_line = self._max_res[0]

        accumulator = 0
        active_pixel_durations = []
        for px in range(components_per_line):
            accumulator += line_active_pixels_samples
            component_samples = accumulator // components_per_line
            active_pixel_durations.append(component_samples)
            accumulator -= component_samples * components_per_line

        line_durations_samples = [h_sync_samples, front_porch_samples] + active_pixel_durations
        line_durations_samples = np.array(line_durations_samples * self._max_res[1])

        im_durations_samples = np.concatenate((header_durations_samples, line_durations_samples))

        return im_durations_samples

    def _px_sin_get(self, pixels_freq_hz: np.array, durations_samples: np.array) -> np.array:
        total_samples = durations_samples.sum()

        result = np.empty(total_samples, dtype=np.float32)
        current_phase = 0
        start_idx = 0

        for i, (freq, samples) in enumerate(zip(pixels_freq_hz, durations_samples)):
            end_idx = start_idx + samples
            result[start_idx:end_idx] = self._signal_gen.sin_gen_samples(
                freq, self._sample_rate_hz, samples,
                amplitude=0.8,
                phase=current_phase
            )
            current_phase = (current_phase + 2 * np.pi * freq * (samples * (1 / self._sample_rate_hz))) % (2 * np.pi)
            start_idx = end_idx

        return result

    def _pixels_get(self) -> np.array:
        status = self._im_proc.im_open(self._filepath)
        if not status:
            return False

        self._im_proc.resolution_check(self._max_res)
        self._im_proc.im_bw_convert()
        return self._im_proc.pixels

    def _pixels_code(self, pixels: np.array) -> np.array:
        pixels_freq_hz = np.vectorize(self._px_freq_hz_get)(pixels).reshape(-1)
        pixels_freq_hz = self._sync_insert(pixels_freq_hz)
        durations_samples = self._durations_get()
        pixels_sin = self._px_sin_get(pixels_freq_hz, durations_samples)
        # plot_build(pixels_sin)
        return pixels_sin

    def _signal_save_wav(self, signal: np.array) -> None:
        signal_int16 = np.int16(signal * 32767)
        wavfile.write('sample.wav', self._sample_rate_hz, signal_int16)

    def code(self) -> None:
        pixels = self._pixels_get()
        signal = self._pixels_code(pixels)
        self._signal_save_wav(signal)

    def decode(self):
        pass
