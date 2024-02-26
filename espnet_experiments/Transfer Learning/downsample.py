from pydub import AudioSegment
import os
import sys

# sys.argv[0] is the name of the script itself
arg1 = sys.argv[1]

for filename in os.listdir(arg1):
    if filename.endswith(".wav"):
        sound = AudioSegment.from_wav(filename)
        sound_w_new_fs = sound.set_frame_rate(22050)
        sound_w_new_fs.export(filename, format="wav")