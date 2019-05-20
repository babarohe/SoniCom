#!/usr/local/src/pyenv/versions/ecsdac/bin/python

"""SMFT通信デモ
Sound Modem
"""

import struct

import wave
import numpy as np

from ecc.rsc import DataProcessor


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

        create_line_signal

        l1.extend(create_line_signal(d1, 0))
        l2.extend(create_line_signal(d2, 1))
        l3.extend(create_line_signal(d3, 2))
        l4.extend(create_line_signal(d4, 3))
        l5.extend(create_line_signal(d5, 4))
        l6.extend(create_line_signal(d6, 5))
        l7.extend(create_line_signal(d7, 6))
        l8.extend(create_line_signal(d8, 7))

        print(d1, d2, d3, d4, d5, d6, d7, d8)

    # サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    swav = np.array(l1) + np.array(l2) + np.array(l3) + np.array(l4) + np.array(l5) + np.array(l6) + np.array(l7) + np.array(l8)

    # FM変調
    # for n in np.arange(t):
    #     np.sin(2*np.pi*fc*t + (1000/44100) * swav)

    swav = [int(x * 32767.0) for x in swav]



    #バイナリ化
    binwave = struct.pack("h" * len(swav), *swav)

    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("output.wav")
    p = (1, 2, 44100, len(binwave), 'NONE', 'not compressed')
    w.setparams(p)
    w.writeframes(binwave)
    w.close()

    upack_data = dp.unpack(packed_data)

    print(upack_data.decode())


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
