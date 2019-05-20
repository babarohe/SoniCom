#!/usr/local/src/pyenv/versions/sonicom/bin/python

"""SMFT通信デモ
Sound Modem
"""

import struct

import wave
import numpy as np
import matplotlib.pylab as plt

from ecc.rsc import DataProcessor

S_RATE      = 44100
CHUNK_TIME  = 256
CENTER_FREQ = 2000

def main():
    dp = DataProcessor()
    packed_data = dp.pack("Hello".encode())

    swav = []

    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    l7 = []
    l8 = []



    for c in packed_data:
        d1 = c & 0x80
        d2 = c & 0x40
        d3 = c & 0x20
        d4 = c & 0x10
        d5 = c & 0x08
        d6 = c & 0x04
        d7 = c & 0x02
        d8 = c & 0x01


        l1.extend(create_line_signal(d1, 0, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l2.extend(create_line_signal(d2, 1, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l3.extend(create_line_signal(d3, 2, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l4.extend(create_line_signal(d4, 3, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l5.extend(create_line_signal(d5, 4, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l6.extend(create_line_signal(d6, 5, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l7.extend(create_line_signal(d7, 6, a=0.2, cf=CENTER_FREQ, fs=S_RATE))
        l8.extend(create_line_signal(d8, 7, a=0.2, cf=CENTER_FREQ, fs=S_RATE))


    swav = multiplex(l1, l2, l3, l4, l5, l6, l7, l8)

    plt.plot(swav[:1024])

    pcm_wav = to_pcm_struct(swav, fs=S_RATE)

    fm_wav = []

    # FM変調
    for n in np.arange(len(swav)):
        f_buf = np.sin(2 * np.pi * 2000 * len(swav) + (1000/2000) * swav[n])

        fm_wav.append(f_buf)

    plt.plot(fm_wav[:1024])
    plt.show()


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
