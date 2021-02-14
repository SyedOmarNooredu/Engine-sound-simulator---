'''Synthesisation of primitive audio building blocks'''

import cfg

import math
import numpy as np
import random

def sine_wave_note(frequency, duration):
    '''
    Creates audio buffer representing a sine-wave
    frequency: Hz
    duration: seconds
    '''
    elements = math.ceil(duration * cfg.sample_rate)
    timesteps = np.linspace(start=0, stop=duration, num=elements, endpoint=False)
    return np.sin(frequency * timesteps * 2 * np.pi)

def sawtooth_wave_note(frequency, duration):
    '''
    Creates audio buffer representing a sine-wave
    frequency: Hz
    duration: seconds
    '''
    elements = math.ceil(duration * cfg.sample_rate)
    timesteps = np.linspace(start=0, stop=duration, num=elements, endpoint=False)
    print(timesteps)
    timesteps = timesteps.tolist()
    timesteps = [1-((x * frequency * 2 * np.pi)%1) for x in timesteps]
    timesteps = np.array(timesteps)
    return frequency * timesteps * 2 * np.pi

def random_wave_note(frequency, duration):
    '''
    Creates audio buffer representing a sine-wave
    frequency: Hz
    duration: seconds
    '''
    elements = math.ceil(duration * cfg.sample_rate)
    timesteps = np.linspace(start=0, stop=duration, num=elements, endpoint=False)
    return np.array([float(x%1)-1 for x in range(len(timesteps))])

def silence(duration):
    '''
    Creates audio buffer representing silence
    duration: seconds
    '''
    elements = math.ceil(duration * cfg.sample_rate)
    return np.zeros(elements)
