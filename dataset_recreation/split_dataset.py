from pathlib import Path
import pathlib
import pandas as pd
import argparse
from constants import MetaDataConstants, TunisianDatasetConstants
from loguru import logger
from tqdm import tqdm
from pydub import AudioSegment


def generate_one_row(duration: float, df: pd.DataFrame, segment: int):
    """Creates a dictionary with information about one audio segment.
    Parameters
    ----------
    duration : float
        The speech duration of the previous audios.
    df : pd.DataFrame
        The dataframe with the data and labels from the tsv file containing metadata.
    segment : int
        The audio's ID.

    Returns
    -------
    element_dict : Dict
        Represents the dataframe row corresponding to one segment.
    duration : float
        The duration of the previous audios added to the duration of one other audio segment.
    """
    element_dict = dict()
    element_dict[MetaDataConstants.SEGMENT_ID_COLUMN_NAME] = df[MetaDataConstants.SEGMENT_ID_COLUMN_NAME][segment]
    audio_path = df[MetaDataConstants.AUDIO_PATH_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.AUDIO_PATH_COLUMN_NAME] = audio_path
    generated_audio = AudioSegment.from_file(audio_path)
    audio_duration = generated_audio.duration_seconds
    element_dict[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME] = df[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.DURATION_COLUMN_NAME] = audio_duration
    element_dict[MetaDataConstants.TARGET_TEXT_COLUMN_NAME] = df[MetaDataConstants.TARGET_TEXT_COLUMN_NAME][segment]
    element_dict[MetaDataConstants.SPEAKER_COLUMN_NAME] = df[MetaDataConstants.SPEAKER_COLUMN_NAME][segment]
    duration += audio_duration
    return element_dict, duration


def split(dataset_dir: pathlib.PosixPath, manifest_root: pathlib.PosixPath, alphabet: str):
    """
    This function split the dataset into 3 subsets according to the speech duration : 7 minutes (~420 sec) for the test,
    10 minutes (~600 sec) for the validation and the rest for the training.
    It generates 3 tsv files from the dataframes : train, validation and test.

    Parameters
    ----------
    dataset_dir : pathlib.PosixPath
        The path to the directory where to find data.
    manifest_root : pathlib.PosixPath
        The path to the directory where to save tsv files.
    alphabet: str

    """
    if alphabet=='phn':
        filename = MetaDataConstants.TSV_FILE_NAME_PHN
    elif alphabet=='bw':
        filename = MetaDataConstants.TSV_FILE_NAME_BW
    else : filename = MetaDataConstants.TSV_FILE_NAME_AR
    df = pd.read_csv(dataset_dir / filename, sep=MetaDataConstants.FILE_SEPARATOR,
                     index_col=0)
    new_dict = dict()
    duration = 0
    test_df, dev_df = False, False
    for segment in tqdm(df.index):
        element_dict, duration = generate_one_row(duration, df, segment)
        new_dict[segment] = element_dict
        if (duration >= TunisianDatasetConstants.TEST_TOTAL_DURATION) and (test_df == False):
            test = pd.DataFrame.from_dict(new_dict, orient='index')
            test.to_csv(manifest_root / MetaDataConstants.TEST_TSV_FILENAME, MetaDataConstants.FILE_SEPARATOR)
            test_df = True
            new_dict = dict()
        if (duration >= (
                TunisianDatasetConstants.TEST_TOTAL_DURATION + TunisianDatasetConstants.VALIDATION_TOTAL_DURATION)) and (
                dev_df == False):
            validation = pd.DataFrame.from_dict(new_dict, orient='index')
            validation.to_csv(manifest_root / MetaDataConstants.VALIDATION_TSV_FILENAME,
                              MetaDataConstants.FILE_SEPARATOR)
            dev_df = True
            new_dict = dict()
    train = pd.DataFrame.from_dict(new_dict, orient='index')
    train.to_csv(manifest_root / MetaDataConstants.TRAIN_TSV_FILENAME, MetaDataConstants.FILE_SEPARATOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", "-d", required=True, type=str)
    parser.add_argument("--output-manifest-root", "-m", required=True, type=str)
    parser.add_argument("--alphabet", "-a", type=str, default='ar')
    args = parser.parse_args()
    dataset_dir = Path(args.data_root).absolute()
    manifest_root = Path(args.output_manifest_root).absolute()
    manifest_root.mkdir(parents=True, exist_ok=True)
    split(dataset_dir, manifest_root, args.alphabet)


if __name__ == "__main__":
    main()
