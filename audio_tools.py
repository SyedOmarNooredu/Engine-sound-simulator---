import cfg

import math
import numpy as np

def concat(bufs):
    return np.hstack(bufs)

def overlay(bufs):
    assert type(bufs) == list and len(bufs), 'bufs must be a non-empty list'
    assert all(len(bufs[0]) == len(buf) for buf in bufs), 'All buffers must have the same length'

    bufs = [np.copy(buf) for buf in bufs]
    for buf in bufs:
        #print(buf)
        buf / len(bufs)

    out_buf = np.sum(bufs, axis=0)
    normalize_volume(out_buf)

    return out_buf

def pad_with_zeros(buf, num_zeros):
    if num_zeros == 0:
        return buf

    return concat([
        buf,
        np.zeros(num_zeros)
    ])

def normalize_volume(buf, loudest_sample=None):
    '''Makes the loudest sample in the buffer use the max_16bit volume. No clipping'''
    buf *= np.int32(cfg.max_16bit / (loudest_sample or find_loudest_sample(buf)))

def exponential_volume_dropoff(buf, duration, base):
    num_samples = math.ceil(duration * cfg.sample_rate)
    zeros_required = len(buf) - num_samples

    unpadded_curve = base / np.logspace(1, 10, num=num_samples, base=base)
    dropoff_curve = pad_with_zeros(unpadded_curve, zeros_required)

    buf *= dropoff_curve

def find_loudest_sample(buf):
    return np.max(np.abs(buf))

def slice(buf, duration):
    '''Take slice of audio buffers based on the duration of sound required'''
    if duration <= 0:
        return []
    num_samples = math.ceil(duration * cfg.sample_rate)
    return buf[:num_samples]

def in_playback_format(buf):
    return buf.astype(np.int16)
