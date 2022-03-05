'''Basic simulation of engine for purposes of audio generation'''
import cfg
import audio_tools

import math
import numpy as np

def _convert_timing_format(timing):
    # Convert timing format from standard format to our internal format.
    # Standard format: each element is the number of crankshaft degrees that cylinder should wait
    #   to fire after the _previous_ cylinder fires
    # Internal format: each element is the number of crankshaft degrees that cylinder should wait
    #   to fire after the _first_ cylinder fires
    timing[0] = 0 # we automatically wait for crank to finish rotation before coming back to first cylinder
    for i in range(1, len(timing)):
        timing[i] += timing[i-1]

class Engine:
    def __init__(self, idle_rpm, limiter_rpm, strokes, cylinders, timing, fire_snd, between_fire_snd, unequal=[]):
        '''
        Note: all sounds used will be concatenated to suit engine run speed.
        Make sure there's excess audio data available in the buffer.

        idle_rpm: engine speed at idle
        limiter_rpm: engine speed at rev limiter
        strokes: number of strokes in full engine cycle, must be 2 or 4 (new: 3 for rotary)
        cylinders: number of cylinders in engine
        timing: array where each element is the number of crankshaft degrees that cylinder should wait
          to fire after the previous cylinder fires. See engine_factory.py for examples
        fire_snd: sound engine should make when a cylinder fires
        between_fire_snd: sound engine should make between cylinders firing
        '''
        # Audio library will request a specific number of samples, but we can't simulate partial engine
        # revolutions, so we buffer whatever we have left over. We start with some zero samples to stop
        # the pop as the audio device opens.
        self._audio_buffer = np.zeros([256])

        self._rpm = idle_rpm
        self.idle_rpm = idle_rpm
        self.limiter_rpm = limiter_rpm

        #assert strokes in (2, 4), 'strokes not in (2, 4), see docstring'
        self.strokes = strokes

        assert cylinders > 0, 'cylinders <= 0'
        self.cylinders = cylinders

        assert len(timing) == cylinders, 'len(timing) != cylinders, see docstring'
        self.timing = timing
        _convert_timing_format(self.timing)

        assert type(fire_snd) == np.ndarray and \
               type(between_fire_snd) == np.ndarray, \
            'Sounds should be passed in as numpy.ndarray buffers'
        assert len(fire_snd) >= cfg.sample_rate * 1 and \
               len(between_fire_snd) >= cfg.sample_rate * 1, \
            'Ensure all audio buffers contain at least 1 second of data, see docstring'
        self.fire_snd = fire_snd
        self.between_fire_snd = between_fire_snd
        
        #added by omar
        if not unequal:
            unequal = [0]*cylinders
        self.unequal = unequal

        self.unequalmore = []
        self.previousms = 0

    def _gen_audio_one_engine_cycle(self):
        # Calculate durations of fire and between fire events
        strokes_per_min = self._rpm * 2 # revolution of crankshaft is 2 strokes
        strokes_per_sec = strokes_per_min / 60
        sec_between_fires = self.strokes / strokes_per_sec
        fire_duration = sec_between_fires / self.strokes # when exhaust valve is open
        between_fire_duration = sec_between_fires / self.strokes * (self.strokes-1) # when exhaust valve is closed

        # Generate audio buffers for all of the cylinders individually
        bufs = []
        bufsunequal = []
        fire_snd = audio_tools.slice(self.fire_snd, fire_duration)
        for cylinder in range(0, self.cylinders):
            unequalms = (
                self.unequal[cylinder]/1000  # unequal converted from milliseconds to seconds
                if self.unequal[cylinder] > 0  # if unequal set
                #else self.unequal[cylinder]  # else 0
                else 0
            )
            #unequalms = min(unequalms, (self.timing[cylinder] / 180) * 2 / strokes_per_sec)
            before_fire_duration = (self.timing[cylinder] / 180) / strokes_per_sec# + unequalms # 180 degrees crankshaft rotation per stroke
            before_fire_snd = audio_tools.slice(self.between_fire_snd, before_fire_duration+unequalms)
            after_fire_duration = between_fire_duration - before_fire_duration # - unequalms
            after_fire_snd = audio_tools.slice(self.between_fire_snd, after_fire_duration)
            #print(len(audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd])))
            if len(self.unequalmore):
                bufsunequal.append(np.array(self.unequalmore))
            if unequalms:  # if unequal parameter set for cylinder
                #print("unequal")
                bufs.append(  # add to buffer
                    np.array(  # make array
                        [0]*len(  # a tring of 0s the length of
                            audio_tools.concat(
                                [
                                    audio_tools.slice(
                                        self.between_fire_snd,
                                        before_fire_duration
                                    ),  # silence as long as before_fire_duration (in seconds)
                                    fire_snd,
                                    after_fire_snd
                                ]  # complete combustion sound including before and after
                            )
                        )
                    )
                )
                #if self.previousms != unequalms:  # unequal ms different from previous cylinder
                before_fire_snd = audio_tools.slice(
                    self.between_fire_snd, # silence
                    before_fire_duration + unequalms# - self.previousms  # current duration plus difference between unequals
                )  # make interval before sound smaller
                bufsunequal.append(
                    audio_tools.concat(
                        [before_fire_snd, fire_snd, after_fire_snd]  # combustion + silence
                    )
                )  # add generated combustion to unequal buffer
                self.previousms = unequalms  # make current unequalms the new previousms
            else:
                #forgot what this was for, probly before separate buffers
                """if self.unequaldelay > len(audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd])):

                    self.unequaldelay -= len(audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd]))
                else:
                    bufsunequal.append(
                        np.array(  # make numpy array of
                            [0]*(  # a list of 0s with the amount of 0s equal to
                                len(  # the length of
                                    audio_tools.slice(self.between_fire_snd, self.unequaldelay)  # silence as long as unequal offset
                                ) 
                                - 
                                len(
                                    audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd])
                                )
                            )
                        )
                    )"""
                bufsunequal.append(
                    np.array(
                        [0]*len(
                            audio_tools.concat(
                                [before_fire_snd, fire_snd, after_fire_snd]  # combustion + silence
                            )
                        )
                    )
                )  # add silence to unequal buffer
                bufs.append(
                    audio_tools.concat(
                        [before_fire_snd, fire_snd, after_fire_snd]  # combustion + silence
                    )
                )  # add combustion package to equal buffer

        # combine both lists
        #print(len(bufs))
        #print("nextone")
        #print(len(bufsunequal))
        #bufs = list(np.maximum(bufs, bufsunequal))
        # Make sure all buffers are the same length (may be off by 1 because of rounding issues)
        
        max_buf_len = len(max(bufs, key=len))
        bufs = [audio_tools.pad_with_zeros(buf, max_buf_len-len(buf)) for buf in bufs]
        
        # same thing as before but with unequal buffer

        max_buf_len_unequal = len(max(bufsunequal, key=len))
        #print(max_buf_len)
        #might not be good idea with unequal, since that's how the unequalness is made
        bufsunequal = [audio_tools.pad_with_zeros(buf, max_buf_len_unequal-len(buf)) for buf in bufsunequal]

        # Combine all the cylinder sounds
        engine_snd = audio_tools.overlay(bufs)  # not sure
        engine_snd_unequal = audio_tools.overlay(bufsunequal)  # not sure
        #print(len(engine_snd), len(engine_snd_unequal))
        if sum(engine_snd_unequal) > 0:  # if unequal buffer contains anything
            if cfg.sound_merge_method == "average":  # average of both buffers
                engine_snd = np.mean([engine_snd, engine_snd_unequal[:len(engine_snd)]], axis=0)
            elif cfg.sound_merge_method == "max":  # maximum values of both buffers
                engine_snd = np.maximum(engine_snd, engine_snd_unequal[:len(engine_snd)])
        if len(engine_snd_unequal) > len(engine_snd):  # if unequal buffer is longer than 
            self.unequalmore = engine_snd_unequal[len(engine_snd):]
        return audio_tools.in_playback_format(engine_snd)

    def gen_audio(self, num_samples):
        '''Return `num_samples` audio samples representing the engine running'''
        # If we already have enough samples buffered, just return those
        if num_samples < len(self._audio_buffer):
            buf = self._audio_buffer[:num_samples]
            self._audio_buffer = self._audio_buffer[num_samples:]
            return buf

        # Generate new samples. If we still don't have enough, loop what we generated
        engine_snd = self._gen_audio_one_engine_cycle()
        while len(self._audio_buffer) + len(engine_snd) < num_samples:
            engine_snd = audio_tools.concat([engine_snd, engine_snd]) # this is unlikely to run more than once

        # Take from the buffer first, and use new samples to make up the difference
        # Leftover new samples become the audio buffer for the next run
        num_new_samples = num_samples - len(self._audio_buffer)
        buf = audio_tools.concat([self._audio_buffer, engine_snd[:num_new_samples]])
        #assert len(buf) == num_samples, (f'${num_samples} requested, but ${len(buf)} samples provided, from ' +
            #f'${len(self._audio_buffer)} buffered samples and ${num_new_samples} new samples')
        self._audio_buffer = engine_snd[num_new_samples:]
        return buf
    
    def throttle(self, fraction):
        '''Applies throttle, increasing or decreasing the engine's RPM based on friction, power etc'''
        if fraction == 1.0:
            if self._rpm < self.limiter_rpm:
                #self._rpm += (1000 / self.strokes)
                self._rpm += (100 / 4)#self.strokes)
            else:
                fraction = 0.0 # cut spark

        if fraction == 0.0:
            if self._rpm > self.idle_rpm:
                #self._rpm -= min(125, self._rpm - self.idle_rpm)
                self._rpm -= min(50, self._rpm - self.idle_rpm)

        #print("\033[A                             \033[A") # clear previous line in console
        print('RPM', self._rpm, end="\r")

    def specific_rpm(self):  # TODO
        '''set to specific RPM, for stuff like RPM sliders or drone simulation'''
        pass
