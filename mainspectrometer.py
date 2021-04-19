import controls
import engine_factory
from audio_device import AudioDevice
import random
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy
import threading

# engine = engine_factory.v_four_90_deg()
# engine = engine_factory.w_16()
# engine = engine_factory.v_8_LS()
# engine = engine_factory.inline_5_crossplane()
# engine = engine_factory.inline_6()
engine = engine_factory.boxer_4_crossplane_custom([1, 1, 0, 0])  # (rando := random.randrange(360)))
# engine = engine_factory.boxer_4_half()
# engine = engine_factory.random()
# engine = engine_factory.fake_rotary_2rotor()

audio_device = AudioDevice()
stream = audio_device.play_stream(engine.gen_audio)

print('\nEngine is running...')
# print(rando)

RATE = 44100
BUFFER = 882

fig = plt.figure()
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line(i):
    data = stream
    data = numpy.log10(numpy.sqrt(
        numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10
    line1.set_data(r, data)
    line2.set_data(numpy.maximum(line1.get_data(), line2.get_data()))
    return (line1,line2)

plt.xlim(0, 20000)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

line_ani = matplotlib.animation.FuncAnimation(
    fig, update_line, init_func=init_line, interval=0, blit=True
)

print(stream)
try:
    #threading.Thread(target=lambda: plt.show()).start()
    plt.show()
    controls.capture_input(engine)  # blocks until user exits
except KeyboardInterrupt:
    pass

print('Exiting...')
stream.close()
audio_device.close()
