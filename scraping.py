import argparse
import json
import pathlib
import sys
from pathlib import Path
from typing import List

import pandas as pd
import pyarabic.araby as araby
import selenium
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

from constants import DerjaNinjaConstants, DrejjaToEnglishDatasetConstants, ScrappedDatasetConstants


def create_driver() -> selenium.webdriver.chrome.webdriver.WebDriver:
    """Creates and returns a Chrome driver instance
    Returns
    -------
    wd : selenium.webdriver.chrome.webdriver.WebDriver
        A Chrome driver instance
    """
    sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    return wd


def remove_diacritics(words: list) -> List:
    """It removes diacritics from a list arabic words.
    Parameters
    ----------
    words : list
        A list of arabic words with diacritics.
    Returns
    -------
    List:
        List of unique words extracted from the input list without diacritics.

    """
    words_without_diacritics = []
    for word in words:
        after_filter = araby.strip_diacritics(word)
        words_without_diacritics.append(after_filter)
    return list(dict.fromkeys(words_without_diacritics))


def tunisian_words_extraction(drejja_to_english_dir: pathlib.PosixPath) -> List:
    """Extracts a list of unique tunisian words from the dataset Drejja_to_english.
    Parameters
    ----------
    drejja_to_english_dir : pathlib.PosixPath
        The directory containing drejja_to_english dataset.
    Returns
    -------
    List:
        The tunisian unique words extracted from drejja_to_english dataset without diacritics.
    """
    tun_sentences = pd.read_csv(drejja_to_english_dir / DrejjaToEnglishDatasetConstants.METADATA_FILE)[
        DrejjaToEnglishDatasetConstants.TUNISIAN_SENTENCES_COLUMN_NAME].tolist()
    words = sum([i.rstrip(".").split(" ") for i in tun_sentences], [])
    return remove_diacritics(words)


def extract_time_from_js_script(scripts: List):
    """Extracts the start and the end times of the term and the sentence from JS scripts
    Parameters
    ----------
    scripts : List
        A list of JS scripts
    Returns
    -------
    start_term : List
        A list containing the start time for each term
    end_term : List
        A list containing the end time for each term
    start_sen : List
        A list containing the start time for each sentence
    end_sen : List
        A list containing the end time for each sentenc
    """
    start_term, end_term, start_sen, end_sen = [], [], [], []
    for script in scripts:
        time_dict = json.loads(script)
        start_term.append(time_dict[DerjaNinjaConstants.TERM][DerjaNinjaConstants.START_TIME])
        end_term.append(time_dict[DerjaNinjaConstants.TERM][DerjaNinjaConstants.END_TIME])
        start_sen.append(time_dict[DerjaNinjaConstants.SENTENCE][DerjaNinjaConstants.START_TIME])
        end_sen.append(time_dict[DerjaNinjaConstants.SENTENCE][DerjaNinjaConstants.END_TIME])
    return start_term, end_term, start_sen, end_sen


def extract_features(results: List):
    """Extracts the link, term , sentence and JS script from the results elements.
    Parameters
    ----------
    results : List
        A list of WebElements.
    Returns
    -------
    audio : list
        A list of audios links.
    terms : list
        A list of terms.
    sentences : list
        A list of sentences.
    scripts : list
        A list of JS scripts.
    """
    audios, terms, sentences, scripts = [], [], [], []
    for result in results:
        audios.append(result.find_element(by=By.TAG_NAME, value=DerjaNinjaConstants.AUDIO_ELEMENT_TAG).get_attribute(
            DerjaNinjaConstants.AUDIO_ELEMENT_ATTRIBUTE))
        terms.append(result.find_element(by=By.CLASS_NAME, value=DerjaNinjaConstants.TERM_CLASS_VALUE).text)
        sentence = result.find_element(by=By.CLASS_NAME,
                                       value=DerjaNinjaConstants.SENTENCE_CLASS_VALUE).find_element(by=By.CLASS_NAME,
                                                                                                    value=DerjaNinjaConstants.EXAMPLE_SENTENCE_CLASS_VALUE)
        sentences.append(sentence.text)
        scripts.append(result.find_element(by=By.TAG_NAME, value=DerjaNinjaConstants.JS_SCRIPT_TAG).get_attribute(
            DerjaNinjaConstants.JS_SCRIPT_ATTRIBUTE))
    return audios, terms, sentences, scripts


def write_one_line(data_root: pathlib.PosixPath, audio_link: str, one_line: str):
    """Verify if the link exists in the text file, if not it adds it.
    Parameters
    ----------
    data_root : pathlib.PosixPath
        The directory where to save the generated text file.
    audio_link : str
        The link of one audio.
    one_line : str
        The line containing the information corresponding to the audio_link.

    """
    with open(data_root / ScrappedDatasetConstants.TEXT_FILE_NAME, "a+") as f, open(
            data_root / ScrappedDatasetConstants.TEXT_FILE_NAME, "r") as file:
        if not (str(audio_link) in file.read()):
            f.write(one_line + '\n')
        else:
            logger.info("link exists")


def scrape_one_page(data_root: pathlib.PosixPath, wd: selenium.webdriver.chrome.webdriver.WebDriver, word: str):
    """Scrapes one search page and write the information corresponding to one link in text file if it does not exist.
    Parameters
    ----------
    data_root : pathlib.PosixPath
        the path where to save the created text file.
    wd : selenium.webdriver.chrome.webdriver.WebDriver
        A Chrome driver instance.
    word : str
       the tunisian word used for the research.
    """
    wd.implicitly_wait(10)
    wd.get(DerjaNinjaConstants.DERJA_NINJA_LINK[0] + str(word) + DerjaNinjaConstants.DERJA_NINJA_LINK[1])
    results = wd.find_elements(by=By.CLASS_NAME, value=DerjaNinjaConstants.RESULT_ELEMENT_CLASS_VALUE)
    audios, terms, sentences, scripts = extract_features(results)
    start_term, end_term, start_sen, end_sen = extract_time_from_js_script(scripts)
    for i in range(len(audios)):
        one_result_line = str(audios[i]) + ScrappedDatasetConstants.TEXT_FILE_SEP + str(
            terms[i]) + ScrappedDatasetConstants.TEXT_FILE_SEP + \
                          str(sentences[i]) + ScrappedDatasetConstants.TEXT_FILE_SEP + str(
            start_term[i]) + ScrappedDatasetConstants.TEXT_FILE_SEP + \
                          str(end_term[i]) + ScrappedDatasetConstants.TEXT_FILE_SEP + str(
            start_sen[i]) + ScrappedDatasetConstants.TEXT_FILE_SEP + \
                          str(end_sen[i])
        write_one_line(data_root, audios[i], one_result_line)


def scrap_all_pages(data_root: pathlib.PosixPath, wd: selenium.webdriver.chrome.webdriver.WebDriver,
                    unique_words: List):
    """Scrapes the search page corresponding to each tunisian word from the list unique_words.
    Parameters
    ----------
    data_root : pathlib.PosixPath
        the path where to save the created text file.
    wd : selenium.webdriver.chrome.webdriver.WebDriver
        A Chrome driver instance.
    unique_words : List
       A list of tunisian words.
    """
    for word in tqdm(unique_words):
        try:
            scrape_one_page(data_root, wd, word)
        except:
            logger.warning("An exception occurred")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--drejja-to-english-metadata-file-path", "-d", required=True, type=str)
    parser.add_argument("--save-data-directory-path", "-s", required=True, type=str)
    args = parser.parse_args()
    data_root = Path(args.save_data_directory_path)
    data_root.mkdir(parents=True, exist_ok=True)
    drejja_to_english_dir = Path(args.drejja_to_english_metadata_file_path)
    web_driver = create_driver()
    unique_words = tunisian_words_extraction(drejja_to_english_dir)
    scrap_all_pages(data_root, web_driver, unique_words)


if __name__ == "__main__":
    main()
