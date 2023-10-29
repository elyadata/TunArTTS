import argparse
import pathlib
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import pyarabic.araby as araby
from loguru import logger
from pydub import AudioSegment
from pydub.utils import mediainfo
from tqdm import tqdm

from constants import MetaDataConstants, ScrappedDatasetConstants, AudioConstants, TunisianDatasetConstants


def convert_mp3_to_wav(audio_name: str, mp3_audio_path: pathlib.PosixPath, start_time: float,
                       save_dir: pathlib.PosixPath) -> Tuple[str, float]:
    """Converts one mp3 audio file to a wav file, it then gets cut according to the given start_time until its end.
    Parameters
    ----------
    audio_name : str
        The audio filename.
    mp3_audio_path : pathlib.PosixPath
        The path of one mp3 audio file.
    start_time : float
        The time when the vaunted words are launched.
    save_dir : pathlib.PosixPath
        The path where to save generated wav file.
    Returns
    -------
    wav_audio_path : pathlib.PosixPath
        The path of the generated audio file.
    duration : float
        The duration of the generated audio file.
    """
    audio = AudioSegment.from_file(mp3_audio_path)
    dst = audio_name.replace('.mp3', '.wav')
    wav_audio_path = save_dir / dst
    chunk = audio[start_time * 1000:]
    chunk.export(wav_audio_path, format="wav")
    generated_audio = AudioSegment.from_file(wav_audio_path)
    duration = generated_audio.duration_seconds
    return wav_audio_path, duration


def clean_text(text: str) -> str:
    """Removes all special characters and diactitics from the text.
    Parameters
    ----------
    text : str
        The text to clean.
    Returns
    -------
    str :
        The input text cleaned and without diacritics.
    """
    char_to_replace_list = MetaDataConstants.CHAR_TO_REPLACE
    for key, value in char_to_replace_list.items():
        text = text.replace(key, value)
    return araby.strip_diacritics(text)


def replace_numbers(audio_number: int, text: str) -> str:
    """Normalizes the text.
    Parameters
    ----------
    audio_number: int
        The ID of one audio.
    text: str
        The text to clean.

    Returns
    -------
    str :
        The normalized text.
    """
    if audio_number == 20914:
        text = text.replace('7', 'سبعة')
    elif audio_number == 18155:
        text = text.replace('3', u'تلاثة')
    elif audio_number == 18989:
        text = text.replace('14', u'اربعطاش')
    elif audio_number == 14934:
        text = text.replace('2016', u'الفين و سطاش')
    return text


def generate_tgt_txt(audio_number: int, term: str, sentence: str) -> str:
    """Align texts to audios
    Parameters
    ----------
    audio_number: int
        The ID of one audio.
    term: str
        The term corresponding to the audio.
    sentence: str
        The sentence corresponding to the audio.
    Returns
    -------
    str :
        The correct text corresponding to the audio segment
    """
    if audio_number in TunisianDatasetConstants.TERM_SEN_SEN_TEXT:
        nbr_terms, nbr_sentences = 1, 2
    elif audio_number in TunisianDatasetConstants.TERM_TERM_SEN_SEN_TEXT:
        nbr_terms, nbr_sentences = 2, 2
    elif audio_number == TunisianDatasetConstants.SEN_SEN_TEXT:
        nbr_terms, nbr_sentences = 0, 2
    elif audio_number == TunisianDatasetConstants.TERM_TERM_TERM_TEXT:
        nbr_terms, nbr_sentences = 3, 0
    elif audio_number in TunisianDatasetConstants.TERM_TERM_TERM_SEN_SEN_SEN_TEXT:
        nbr_terms, nbr_sentences = 3, 3
    else:
        nbr_terms, nbr_sentences = 3, 2
    text = ' '.join([term] * nbr_terms) + ' ' + ' '.join([sentence] * nbr_sentences)
    if audio_number == 19888:
        number = 'ثمنية و ثمانين'
        text = number + ' ' + text
    if audio_number in [20914, 18155, 18989, 14934]:
        return replace_numbers(audio_number, text)
    return text


def generate_one_row(audio_number: int, wav_path: pathlib.PosixPath, df: pd.DataFrame, segment: int, sample_rate: int,
                     duration: float) -> Dict:
    """Creates a dictionary with information about one audio segment.
    Parameters
    ----------
    audio_number: int
        The ID of one audio.
    wav_path: pathlib.PosixPath
        The path of one audio file.
    df : pd.DataFrame
        The dataframe with the data and labels from the tsv file containing metadata.
    segment : int
        The segment id.
    sample_rate: int
        The sample rate.
    duration: float
        The duration of one audio in seconds.
    Returns
    ----------
    Dict
        Represents the dataframe row corresponding to one segment.
    """
    element_dict = dict()
    element_dict[MetaDataConstants.SEGMENT_ID_COLUMN_NAME] = audio_number
    element_dict[MetaDataConstants.AUDIO_PATH_COLUMN_NAME] = str(wav_path)
    element_dict[MetaDataConstants.SAMPLE_RATE_COLUMN_NAME] = sample_rate
    element_dict[MetaDataConstants.SPEAKER_COLUMN_NAME] = MetaDataConstants.SPEAKER
    element_dict[MetaDataConstants.DURATION_COLUMN_NAME] = duration
    term = df[MetaDataConstants.TERM_COLUMN_NAME][segment]
    sentence = df[MetaDataConstants.SENTENCE_COLUMN_NAME][segment]
    text = generate_tgt_txt(audio_number, term, sentence)
    text = clean_text(text)
    element_dict[MetaDataConstants.TARGET_TEXT_COLUMN_NAME] = text
    return element_dict


def tunisian_dataset_generation(mp3_files_dir: pathlib.PosixPath, df: pd.DataFrame,
                                save_dataset_dir: pathlib.PosixPath):
    """Given the scrapped information and the downloaded mp3 audios, it creates a new dataset and generates the appropriate tsv file.
    Parameters
    ----------
    mp3_files_dir: pathlib.PosixPath
        The path where to find the downloaded mp3 files.
    df: pd.DataFrame
        The dataframe with the data and labels from the file containing metadata.
    save_dataset_dir: pathlib.PosixPath
        The path where to save the generated dataset.

    """
    save_dir = save_dataset_dir / f"wav"
    save_dir.mkdir(parents=True, exist_ok=True)
    new_dict = dict()
    for segment in tqdm(df.index):
        try:
            audio_name = df[MetaDataConstants.AUDIO_PATH_COLUMN_NAME][segment].split('/')[-1]
            audio_number = int(audio_name.replace('.mp3', ''))
            mp3_audio_path = mp3_files_dir / audio_name
            sample_rate = int(mediainfo(mp3_audio_path)["sample_rate"])
            if (sample_rate == AudioConstants.SAMPLE_RATE) or (sample_rate == 48000):
                start = df[ScrappedDatasetConstants.TERM_START_TIME][segment]
                wav_audio_path, duration = convert_mp3_to_wav(audio_name, mp3_audio_path, start, save_dir)
                new_dict[segment] = generate_one_row(audio_number, wav_audio_path, df, segment, sample_rate, duration)
        except:
            logger.error("audio does not exist")

    new_df = pd.DataFrame.from_dict(new_dict, orient='index')
    new_df.to_csv(save_dataset_dir / MetaDataConstants.TSV_FILE_NAME_AR, sep=MetaDataConstants.FILE_SEPARATOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--txt-file-path", "-txt", required=True, type=str)
    parser.add_argument("--mp3-files-path", "-w", required=True, type=str)
    parser.add_argument("--save-data-directory-path", "-div", required=True, type=str)
    args = parser.parse_args()
    metadata_path = Path(args.txt_file_path)
    data_root = Path(args.save_data_directory_path)
    data_root.mkdir(parents=True, exist_ok=True)
    mp3_files_dir = Path(args.mp3_files_path)
    df = pd.read_csv(metadata_path / ScrappedDatasetConstants.TEXT_FILE_NAME,
                     sep=ScrappedDatasetConstants.TEXT_FILE_SEP, header=None,
                     names=ScrappedDatasetConstants.COLUMN_NAMES)
    tunisian_dataset_generation(mp3_files_dir, df, data_root)


if __name__ == "__main__":
    main()
