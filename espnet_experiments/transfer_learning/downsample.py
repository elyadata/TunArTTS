from pydub import AudioSegment
import os
import sys
from tqdm import tqdm
# sys.argv[0] is the name of the script itself
arg1 = sys.argv[1]

for filename in tqdm(os.listdir(arg1)):
    if filename.endswith(".wav"):
        sound = AudioSegment.from_wav(f'{arg1}/{filename}')
        sound_w_new_fs = sound.set_frame_rate(22050)
        sound_w_new_fs.export(f'{arg1}/{filename}', format="wav")
