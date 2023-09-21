import os
from os.path import exists
import time
import argparse
import pathlib
import pandas as pd
import requests
from loguru import logger
from pathlib import Path
from tqdm import tqdm
from constants import ScrappedDatasetConstants


def download(url: str, filename: str, save_dir):
    """Downloads one audio file
    Parameters
    ----------
    url: str
        The link of the audio file
    filename: str
        The audio filename
    save_dir: pathlib.PosixPath
        The path where to save the downloaded audios

    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}

    file_path = save_dir / filename
    request = requests.get(url, stream=True, headers=headers)
    if request.ok:
        with open(file_path, 'wb') as f:
            for chunk in request.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        logger.error("Download failed: status code {}\n{}".format(request.status_code, request.text))


def download_multiple(df: pd.DataFrame, save_dir: pathlib.PosixPath):
    """Downloads multiple audio files and skip the existing ones
    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the data and labels from the tsv file containing metadata.
    save_dir: pathlib.PosixPath
        The path where to save the downloaded audios

    """
    for segment in tqdm(df.index):
        video_name = df[ScrappedDatasetConstants.COLUMN_NAMES[0]][segment]
        name = video_name.split('/')[-1]
        video_path = str(save_dir / name)
        if exists(video_path):
            logger.warning("File: {} alredy exists. Skipping download".format(video_name))
        else:
            try:
                download(video_name, name, save_dir)
            except:
                logger.error("Could not download file: {} at {}".format(name, video_name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--txt-file-path", "-txt", required=True, type=str)
    parser.add_argument("--save-data-directory-path", "-s", required=True, type=str)
    args = parser.parse_args()
    dataset_path = Path(args.txt_file_path)
    data_root = Path(args.save_data_directory_path)
    data_root.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(dataset_path / ScrappedDatasetConstants.TEXT_FILE_NAME, sep=ScrappedDatasetConstants.TEXT_FILE_SEP,
                     names=ScrappedDatasetConstants.COLUMN_NAMES)
    download_multiple(df, data_root)


if __name__ == "__main__":
    main()
