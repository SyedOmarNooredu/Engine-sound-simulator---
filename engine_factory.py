# Reference: https://en.wikipedia.org/wiki/Big-bang_firing_order

import synth
import audio_tools
from engine import Engine
import random as rd

_fire_snd = synth.sine_wave_note(frequency=160, duration=1)
audio_tools.normalize_volume(_fire_snd)
audio_tools.exponential_volume_dropoff(_fire_snd, duration=0.06, base=5)

def v_twin_90_deg():
    '''Suzuki SV650/SV1000, Yamaha MT-07'''
    return Engine(
        idle_rpm=1000,
        limiter_rpm=10500,
        strokes=4,
        cylinders=2,
        timing=[270, 450],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def v_twin_60_deg():
    return Engine(
        idle_rpm=1100,
        limiter_rpm=10500,
        strokes=4,
        cylinders=2,
        timing=[300, 420],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def v_twin_45_deg():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=2,
        timing=[315, 405],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_4():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=4,
        timing=[180, 180, 180, 180],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_7():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=7,
        timing=[103, 103, 103, 103, 103, 103, 102],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_6():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=6,
        timing=[120, 120, 120, 120, 120, 120],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )
def v_8_LR():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[90]*8,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def v_8_LS():
    return Engine(
        idle_rpm=600,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[180, 270, 180, 90, 180, 270, 180, 90],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def v_8_FP():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[180]*8,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def v_8_FP_TVR():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[75]*8,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def w_16():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=16,
        timing=[27, 90-27, 27, 180-117, 27, 270-207, 27, 360-297, 27, 90-27, 27, 180-117, 27, 270-207, 27, 360-297],
        #timing=[180, 270, 180, 90],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_9():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=9,
        timing=[80]*9,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_1():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=1,
        timing=[720],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_7_4_3():
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=7,
        timing=[180, 90, 180, 270]+[240]*3,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_16():
    whynot=16
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=whynot,
        timing=[720/whynot]*whynot,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_5():
    whynot=5
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=[720/whynot]*whynot,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_any():
    whynot=5
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=[720/whynot]*whynot,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_5_crossplane():
    whynot=5
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=[180, 90, 180, 90, 180],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_4_uneven_firing():
    whynot=4
    mini = 170
    maxi = 190
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=whynot,
        timing=[rd.uniform(mini, maxi), rd.uniform(mini, maxi), rd.uniform(mini, maxi), rd.uniform(mini, maxi)],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def boxer_4_crossplane_custom(rando=[0]*4):
    whynot=4
    because=180
    #because=rando
    return Engine(
        idle_rpm=750,
        limiter_rpm=6700,
        strokes=4,
        cylinders=whynot,
        timing=[because, 360-because]*2,
        #timing = [180, 270, 180, 90],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1),
        unequal=rando
    )

def boxer_4_half():
    whynot=2
    return Engine(
        idle_rpm=800,
        limiter_rpm=6700,
        strokes=4,
        cylinders=whynot,
        timing=[180, 180],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def random():
    #whynot=rd.choice([4, 8, 16])
    whynot=4
    print(whynot)
    randlist = []
    for i in range(whynot):
        rando = rd.randrange(int(360/5/whynot), int(1440/5/whynot))*5
    randlist = [rd.randrange(int(360/5/whynot), int(1440/5/whynot))*5 for x in range(whynot)]
    print(randlist)
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=randlist,
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def v_four_90_deg():
    return Engine(
        idle_rpm=1100,
        limiter_rpm=16500,
        strokes=4,
        cylinders=4,
        timing=[180, 90, 180, 270],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def fake_rotary_2rotor():
    difference = 60*(4*3)
    return Engine(
        idle_rpm=100,
        limiter_rpm=8300,
        strokes=1/3,
        cylinders=2,
        #timing=[720/8]*2,
        timing = [difference, 720-difference],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )

def inline_4_1_spark_plug_disconnected():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=3,
        timing=[180, 360, 180],
        fire_snd=_fire_snd,
        between_fire_snd=synth.silence(1)
    )
