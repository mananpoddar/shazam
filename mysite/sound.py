import sounddevice as sd
import numpy as np
duration = 5  # seconds
fs=11500
sd.default.samplerate = fs
sd.default.channels = 2
myarray = sd.rec(int(duration * fs),blocking=True)
print("RECORDING AUDIO")
print(myarray)
print("AUDIO RECODING COMPLETE ")
sd.play(myarray, fs)
sd.wait()
print("PLAYING COMPELETE")





