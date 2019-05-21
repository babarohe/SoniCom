
import numpy as np

SAMPLING_RATE = 44100

class SignalGenerator():
    def __init__(self, center_freq, clock_samples=1024, sampling_rate=SAMPLING_RATE):
        self._center_freq = center_freq
        self._clock_samples = clock_samples
        self._sampling_rate = sampling_rate

    @property
    def sampling_rate(self):
        return self._sampling_rate

    def generate(self, packed_data):
        stream_length = len(packed_data)

        data_streams  = self._data_stream_line_spliter(packed_data)

        enable_stream = []
        for _ in range(stream_length):
            enable_stream.extend(self._generate(True, 2000))

        stream = self._multiplexer(*data_streams)

        return stream


    def _data_stream_line_spliter(self, packed_data):
        band = 8
        stream = []

        for word in packed_data:
            line_cycle = [None for _ in range(band)]
            for l_num in range(band):
                bit = word & (0x80 >> l_num)

                signal = self._generate(bit, 100 * (l_num * 1.2))
                line_cycle[l_num] = signal

            stream.append(line_cycle)

        return stream


    def _generate(self, bit, freq, gain=0.25):
        line_signal = [0.0 for _ in range(self._clock_samples)]

        if not bit:
            freq = 0.0

        for n in np.arange(self._clock_samples):
            s = gain * np.sin(2.0 * np.pi * freq * n / self._sampling_rate)

            line_signal[n] = s

        return line_signal


    def _multiplexer(self, *signals):
        formulas = []

        print(len(signals))

        for i in range(len(signals)):
            formulas.append(f"np.array(signals[{i}])")

        swav = eval(" + ".join(formulas))

        return swav
