#!/usr/bin/env python

from __future__ import print_function, division
import argparse
import numpy as np
import comtypes.client
import scipy.io.wavfile as wavf


def tts(text, dest):
    """
    https://stackoverflow.com/questions/49871252/saving-text-to-speech-python
    """
    speak = comtypes.client.CreateObject("SAPI.SpVoice")
    filestream = comtypes.client.CreateObject("SAPI.spFileStream")
    filestream.open(dest, 3, False)
    speak.AudioOutputStream = filestream
    speak.Speak(text)
    filestream.close()


def pad(data, n_pad):
    """
    https://stackoverflow.com/questions/32468349/how-to-add-silence-in-front-of-a-wav-file/32477869#32477869
    """
    shape = (n_pad,) + data.shape[1:]
    if shape[0] > 0:
        p = np.zeros(shape, np.int16)  # キャストが無いと音声再生不可
        return np.vstack((p, data)) if len(shape) > 1 else np.hstack((p, data))
    else:
        return data


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str)
    parser.add_argument('seconds', type=int)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    dest = '%s__%dsecs.wav' % (args.text, args.seconds)

    tts(args.text, dest)
    sample_rate, in_data = wavf.read(dest)
    out_data = pad(in_data, int(sample_rate * args.seconds))
    wavf.write(dest, sample_rate, out_data)
