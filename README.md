# Engine Sound Simulator+++

Indirect fork of [engine sound simulator by jgardner8](https://github.com/jgardner8/engine-sound-simulator "Original repository")

## Changes
* Throttle key activation now works (using pynput)
* More engines in engine_factory.py
* random and sawtooth waves in synth.py
* "Subie rumble" (a.k.a unequal exhaust sound)(WIP)
* Rotary (WIP)(need to allow 2/3 strokes)
## Requirements
* Functioning audio playback devices
* Python
* Operating System compatible with Python and audio devices
## Setup
```
pip install -r requirements.txt --user
```
Alternatively, you can run 'Install Requirements.bat'.
## Run
Double-click 'main.py' or enter
```
python main.py
```
into Command Prompt/a terminal to run the script.
## Troubleshooting
If there is a problem with installing pyaudio, consult [this StackOverflow answer](https://stackoverflow.com/a/55630212/13015676)
## Credit
[jgardner](https://github.com/jgardner8 "Original Creator") made the original and therefore most of this repository. Thanks man.
