from pydub import AudioSegment
import os

for filename in os.listdir("./downloads/dataset-tun/wav"):
    if filename.endswith(".wav"):
        sound = AudioSegment.from_wav(filename)
        sound_w_new_fs = sound.set_frame_rate(22050)
        sound_w_new_fs.export(filename, format="wav")