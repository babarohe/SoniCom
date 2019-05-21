
import numpy as np
import matplotlib.pylab as plt


SAMPLING_RATE = 44100

class SignalGenerator():
    def __init__(self, center_freq, clock_samples=512, sampling_rate=SAMPLING_RATE):
        self._center_freq = center_freq
        self._clock_samples = clock_samples
        self._sampling_rate = sampling_rate

    @property
    def sampling_rate(self):
        return self._sampling_rate


    def generate(self, packed_data):
        stream_length = len(packed_data)

        data_streams  = self._data_stream_line_spliter(packed_data)

        # plt.plot(data_streams[0][1024:4096])
        # plt.plot(data_streams[1][1024:4096])
        # plt.plot(data_streams[2][1024:4096])
        # plt.plot(data_streams[3][1024:4096])
        # plt.plot(data_streams[4][1024:4096])
        # plt.plot(data_streams[5][1024:4096])
        # plt.plot(data_streams[6][1024:4096])
        # plt.plot(data_streams[7][1024:4096])
        # plt.show()


        enable_stream = []
        for _ in range(stream_length):
            enable_stream.extend(self._generate(True, 200))

        stream = self._multiplexer(*data_streams)

        plt.plot(stream[1024:4096])
        plt.show()


        return stream


    def _data_stream_line_spliter(self, packed_data):
        band = 8
        stream = [[] for _ in range(band)]

        for word in packed_data:

            for l_num in range(band):
                bit = word & (0x80 >> l_num)

                signal = self._generate(bit, 600 + 10 * (1.5 * l_num))
                stream[l_num].extend(signal)

        return stream


    def _generate(self, bit, freq, gain=0.2):
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
