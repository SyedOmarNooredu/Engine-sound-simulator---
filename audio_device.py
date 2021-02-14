import cfg

import pyaudio

class AudioDevice:
    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()

    def close(self):
        self._pyaudio.terminate()

    def play_stream(self, callback):
        def callback_wrapped(in_data, frame_count, time_info, status_flags):
            return (callback(frame_count), pyaudio.paContinue)

        return self._pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=cfg.sample_rate,
            output=True,
            stream_callback=callback_wrapped
        )
