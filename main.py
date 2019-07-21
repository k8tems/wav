#!/usr/bin/env python

from __future__ import print_function, division
import scipy.io.wavfile as wavf
import numpy as np
from sys import argv
import comtypes.client


def tts(text, dest):
    speak = comtypes.client.CreateObject("SAPI.SpVoice")
    filestream = comtypes.client.CreateObject("SAPI.spFileStream")
    filestream.open(dest, 3, False)
    speak.AudioOutputStream = filestream
    speak.Speak(text)
    filestream.close()


def pad(data, n_pad):
    """
    下記のコードを動くように修正
    https://stackoverflow.com/questions/32468349/how-to-add-silence-in-front-of-a-wav-file/32477869#32477869
    """
    shape = (n_pad,) + data.shape[1:]
    if shape[0] > 0:
        p = np.zeros(shape, np.int16)  # キャストが無いと音声再生不可
        return np.vstack((p, data)) if len(shape) > 1 else np.hstack((p, data))
    else:
        return data


if __name__ == "__main__":
    if len(argv) != 2:
        print("Wrong arguments.")
    else:
        n_secs = int(argv[1])

        text = 'スタンス'
        dest = '%s__%dsecs.wav' % (text, n_secs)
        tts(text, dest)

        sample_rate, in_data = wavf.read(dest)
        print("Padding with %s seconds of silence" % str(n_secs))
        out_data = pad(in_data, int(sample_rate * n_secs))
        wavf.write(dest, sample_rate, out_data)
