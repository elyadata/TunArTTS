import argparse
import pathlib
from pathlib import Path
from typing import Dict

import pandas as pd
from tqdm import tqdm

from constants import BuckwalterMapping
from constants import MetaDataConstants


def arabicToBuckwalter(word: str) -> str:
    """Converts input arabic word to Buckwalter
    Parameters
    ----------
    word : str
        The arabic word to convert.
    Returns
    -------
    str
        The word converted to buckwalter
    """
    res = ''
    for letter in word:
        if letter in BuckwalterMapping.BUCKWALTER:
            res += BuckwalterMapping.BUCKWALTER[letter]
        else:
            res += letter
    return res


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
        represents the dataframe row corresponding to one segment.

    """
    element_dict = dict()
    element_dict[MetaDataConstants.SEGMENT_ID_COLUMN_NAME] = df[MetaDataConstants.SEGMENT_ID_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.AUDIO_PATH_COLUMN_NAME] = df[MetaDataConstants.AUDIO_PATH_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME] = df[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.SPEAKER_COLUMN_NAME] = df[MetaDataConstants.SPEAKER_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.DURATION_COLUMN_NAME] = df[MetaDataConstants.DURATION_COLUMN_NAME][segment]
    text = df[MetaDataConstants.TARGET_TEXT_COLUMN_NAME][segment]
    bw_text = ''
    for word in text.split():
        bw_text += arabicToBuckwalter(word) + ' '
    element_dict[MetaDataConstants.TARGET_TEXT_COLUMN_NAME] = bw_text
    return element_dict


def dataset_conversion(data_dir: pathlib.PosixPath, df: pd.DataFrame):
    """Converts the texts of the dataset from arabic letter to Buckwalter and save the generated dataframe in a new tsv file.
    Parameters
    ----------
    data_dir : pathlib.PosixPath
        The path where to save the generated tsv file.
    df : pd.DataFrame
        The dataframe with the data and labels from the tsv file containing metadata.
    """
    new_dict = dict()
    for segment in tqdm(df.index):
        new_dict[segment] = generate_one_row(df, segment)
    new_df = pd.DataFrame.from_dict(new_dict, orient='index')
    new_df.to_csv(data_dir / MetaDataConstants.TSV_FILE_NAME_BW, sep=MetaDataConstants.FILE_SEPARATOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir-path", "-d", required=True, type=str)
    args = parser.parse_args()
    data_dir = Path(args.dataset_dir_path)
    df = pd.read_csv(data_dir / MetaDataConstants.TSV_FILE_NAME_AR, sep=MetaDataConstants.FILE_SEPARATOR)
    dataset_conversion(data_dir, df)


if __name__ == "__main__":
    main()
