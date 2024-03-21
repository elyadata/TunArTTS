import argparse
import os
import pathlib
import sys
from pathlib import Path

import pandas as pd
from typing import List

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from constants import *


def find_tsv_filename(tsv_files_path: str, suffix=".tsv") -> List[str]:
    """
    This function browses the directory containing tsv files and returns a list of tsv filenames.
    Parameters
    ----------
    tsv_files_path : str
        The path of the directory containing tsv files.
    suffix : str
        Files extension (default is ".tsv").

    Returns
    -------
    List
        a list of tsv filenames.
    """
    filenames = os.listdir(tsv_files_path)
    return [filename for filename in filenames if filename.endswith(suffix)]


def create_text_file(save_dir: pathlib.PosixPath, file: str):
    """Creates the file that describes the mapping from an utterance-ID to a text
    Parameters
    ---------
    file : str
        the name of one tsv file.
    save_dir : pathlib.PosixPath
        the path where to save the created file
    """
    df = pd.read_csv(file, sep=Constant.FILE_SEPARATOR)
    with open(save_dir / EspnetConstants.UTT_TO_TEXT_FILE, "w") as fp:
        for i in df.index:
            line = str(df[Constant.SEGMENT_ID_COLUMN_NAME][i]) + " " + df[Constant.TARGET_TEXT_COLUMN_NAME][i] + '\n'
            fp.write(line)


def create_spk2utt_file(save_dir: pathlib.PosixPath, file: str):
    """Creates the file that describes the mapping from a speaker-ID to a list of utterance-IDs
    Parameters
    ---------
    file : str
        the name of one tsv file.
    save_dir : pathlib.PosixPath
        the path where to save the created file

    """
    df = pd.read_csv(file, sep=Constant.FILE_SEPARATOR)
    utt_list = []
    for i in df.index:
        utt_list.append(str(df[Constant.SEGMENT_ID_COLUMN_NAME][i]))
    utterances = ' '.join(utt_list)
    with open(save_dir / EspnetConstants.SPEAKER_TO_UTT_FILE, "w") as fp:
        speaker = df[Constant.SPEAKER_COLUMN_NAME][1]
        speaker = speaker.replace(' ', '_')
        line = speaker + " " + utterances + '\n'
        fp.write(line)


def create_utt2spk_file(save_dir: pathlib.PosixPath, file: str):
    """Creates the file that describes the mapping from an utterance-ID to a speaker-ID
    Parameters
    ---------
    file : str
        the name of one tsv file.
    save_dir : pathlib.PosixPath
        the path where to save the created file
    """
    df = pd.read_csv(file, sep=Constant.FILE_SEPARATOR)
    with open(save_dir / EspnetConstants.UTT_TO_SPEAKER_FILE, "w") as fp:
        for i in df.index:
            speaker = df[Constant.SPEAKER_COLUMN_NAME][i]
            speaker = speaker.replace(' ', '_')
            line = str(df[Constant.SEGMENT_ID_COLUMN_NAME][i]) + " " + speaker + '\n'
            fp.write(line)


def create_wav_scp_file(save_dir: pathlib.PosixPath, file: str):
    """Creates the file that describes the mapping from an utterance-ID to a path of audio file
        Parameters
        ---------
        dataset_path : str
            The path where to find the dataset directory
        file : str
            the name of one tsv file.
        save_dir : pathlib.PosixPath
            the path where to save the created file
        """
    df = pd.read_csv(file, sep=Constant.FILE_SEPARATOR)
    with open(save_dir / EspnetConstants.UTT_TO_PATH_FILE, "w") as fp:
        for i in df.index:
            line = str(df[Constant.SEGMENT_ID_COLUMN_NAME][i]) + " " + df[Constant.AUDIO_PATH_COLUMN_NAME][i] + '\n'
            fp.write(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tsv-files-path", "-d", required=True, type=str)
    parser.add_argument("--save-data-directory-path", "-s", required=True, type=str)
    args = parser.parse_args()
    data_root = Path(args.save_data_directory_path)
    data_root.mkdir(parents=True, exist_ok=True)
    filenames = find_tsv_filename(args.tsv_files_path)
    for file in filenames:
        if (Constant.TRAIN_SPLIT in file):
            split = Constant.TRAIN_SPLIT
        elif (Constant.DEV_SPLIT in file):
            split = Constant.DEV_SPLIT
        elif (Constant.TEST_SPLIT in file):
            split = Constant.TEST_SPLIT
        split_dir_path = str(data_root) + '/' + split
        save_dir = Path(split_dir_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        create_wav_scp_file(save_dir, str(args.tsv_files_path) + '/' + file)
        create_text_file(save_dir, str(args.tsv_files_path) + '/' + file)
        create_utt2spk_file(save_dir, str(args.tsv_files_path) + '/' + file)
        create_spk2utt_file(save_dir, str(args.tsv_files_path) + '/' + file)


if __name__ == "__main__":
    main()
