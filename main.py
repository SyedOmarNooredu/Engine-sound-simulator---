import controls
import engine_factory
from audio_device import AudioDevice
import random

#engine = engine_factory.v_four_90_deg()
#engine = engine_factory.w_16()
#engine = engine_factory.v_8_LS()
#engine = engine_factory.inline_5_crossplane()
engine = engine_factory.boxer_4_crossplane_custom([4, 4, 0, 0])#(rando := random.randrange(360)))
#engine = engine_factory.boxer_4_half()
#engine = engine_factory.random()

audio_device = AudioDevice()
stream = audio_device.play_stream(engine.gen_audio)

print('\nEngine is running...')
#print(rando)

try:
    controls.capture_input(engine) # blocks until user exits
except KeyboardInterrupt:
    pass

print('Exiting...')
stream.close()
audio_device.close()
