import argparse
import os
from pathlib import Path

from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

from constants import Trim_silences


def trim_silence(path: str, save_dir: Path):
    """
    Trimming silences and then exporting a file with the same name minus the silences.

    Args:
      path (str): A full path to the audio file to be trimmed.

    Returns:
      This function doesn't return anything.
    """
    # Variables for the audio file
    file_name = path.split('/')[-1]
    audio_format = Trim_silences.audio_format

    # Reading and splitting the audio file into chunks
    sound = AudioSegment.from_file(path, format=audio_format)
    audio_chunks = split_on_silence(sound
                                    , min_silence_len=Trim_silences.min_silence_len
                                    , silence_thresh=Trim_silences.silence_thresh
                                    , keep_silence=Trim_silences.keep_silence
                                    )

    # Putting the file back together
    combined = AudioSegment.empty()
    for chunk in audio_chunks:
        combined += chunk
    combined.export(f'{save_dir}/{file_name}', format=audio_format)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--audios-path", "-audio", required=True, type=str)
    parser.add_argument("--save-data-directory-path", "-s", required=True, type=str)
    args = parser.parse_args()
    dataset_path = str(args.audios_path)
    save_dir = Path(args.save_data_directory_path)
    for filename in tqdm(os.listdir(dataset_path)):
        if filename.endswith(".wav"):
            trim_silence(dataset_path + '/' + filename, save_dir)
