#!/usr/local/src/pyenv/versions/sonicom/bin/python

"""SMFT通信デモ
Sound Modem
"""

import struct

import wave
import numpy as np
import matplotlib.pylab as plt

from issb.presentation import Presentation
from issb.signal_generator import SignalGenerator


S_RATE      = 44100
CHUNK_TIME  = 256
CENTER_FREQ = 2000

def main():
    dp = Presentation()
    packed_data = dp.pack("0".encode())

    sg = SignalGenerator(1200)
    stream = sg.generate(packed_data)



    # FM変調
    # for n in np.arange(len(swav)):
    #     f_buf = np.sin(2 * np.pi * 2000 * len(swav) + (1000/2000) * swav[n])

    #     fm_wav.append(f_buf)

    pcm_wav = to_pcm_struct(stream, sg.sampling_rate)
    # plt.plot(swav[500:600])
    # plt.plot(fm_wav[500:1500])
    # plt.show()


    #バイナリ化
    binwave = struct.pack("h" * len(pcm_wav), *pcm_wav)

    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("output.wav")
    p = (1, 2, CENTER_FREQ, len(binwave), 'NONE', 'not compressed')
    w.setparams(p)
    w.writeframes(binwave)
    w.close()

    upack_data = dp.unpack(packed_data)

    print(upack_data.decode())


def multiplex(*lines):
    formulas = []
    for i in range(len(lines)):
        formulas.append(f"np.array(lines[{i}])")

    swav = eval(" + ".join(formulas))

    return swav


def to_pcm_struct(swav, fs):

    return [int(x * (fs / 2.0)) for x in swav]


def create_line_signal(data, linenum, a=0.2, cf=1200, fs=44100, t=256):
    swav = []

    if not data:
        cf = 0.0

    for n in np.arange(t):
        s = a * np.sin(2.0 * np.pi * cf * (1.0525 * linenum) * n / fs)

        swav.append(s)

    return swav

def merge(*lines):
    pass

if __name__ == '__main__':
    main()
