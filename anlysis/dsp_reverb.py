import wave
import pysndfx


with wave.open('input_file.wav', 'rb') as wav:
    params = wav.getparams()
    frames = wav.readframes(wav.getnframes())

fx = pysndfx.AudioEffectsChain()
fx.reverb()

output_frames = fx.apply(frames, params[0], params[1], params[2])

with wave.open('output_file.wav', 'wb') as wav:
    wav.setparams(params)
    wav.writeframes(output_frames)