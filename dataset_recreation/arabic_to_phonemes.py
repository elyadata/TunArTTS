import sys
import pandas as pd
from constants import MetaDataConstants
from tqdm import tqdm
from arabic_pronounce import phonetise
from typing import Dict
from pathlib import Path
from os import path
import pathlib
import argparse


def arabic_to_phonemes(tgt_text: str) -> str:
    """Converts the arabic text to phonemes
    Parameters
    ----------
    tgt_text : str
        The tet to convert
    Returns
    -------
    str
        The phonemes corresponding to the text.
    """
    phonemes = []
    for word in tgt_text.split():
        phonemes.append(phonetise(word)[0])
    return ' '.join(phonemes)


def generate_one_row(df: pd.DataFrame, segment: int) -> Dict:
    """Creates a dictionary with information about one audio segment.
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe with the data and labels from the tsv file containing metadata.
    segment : int
        The segment id.

    Returns
    ----------
    Dict
        Represents the dataframe row corresponding to one segment.
    """
    element_dict = dict()
    element_dict[MetaDataConstants.SEGMENT_ID_COLUMN_NAME] = df[MetaDataConstants.SEGMENT_ID_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.AUDIO_PATH_COLUMN_NAME] = df[MetaDataConstants.AUDIO_PATH_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME] = df[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.SPEAKER_COLUMN_NAME] = df[MetaDataConstants.SPEAKER_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.DURATION_COLUMN_NAME] = df[MetaDataConstants.DURATION_COLUMN_NAME][segment]
    text = df[MetaDataConstants.TARGET_TEXT_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.TARGET_TEXT_COLUMN_NAME] = arabic_to_phonemes(text)
    return element_dict


def dataset_text_conversion(data_dir: pathlib.PosixPath):
    """Converts all the texts in the dataset from arabic letter to phonemes using Nawar's phonemiser.
    Parameters
    ----------
    data_dir : pathlib.PosixPath
        The path to the dataset directory.

    """
    df = pd.read_csv(data_dir / MetaDataConstants.TSV_FILE_NAME_AR, sep=MetaDataConstants.FILE_SEPARATOR)
    new_dict = dict()
    for segment in tqdm(df.index):
        new_dict[segment] = generate_one_row(df, segment)
    new_df = pd.DataFrame.from_dict(new_dict, orient='index')
    new_df.to_csv(data_dir / MetaDataConstants.TSV_FILE_NAME_PHN, sep=MetaDataConstants.FILE_SEPARATOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", "-d", required=True, type=str)
    args = parser.parse_args()
    data_root = Path(args.data_root)
    dataset_text_conversion(data_root)


if __name__ == "__main__":
    main()
