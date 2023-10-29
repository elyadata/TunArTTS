# TTS-Dataset-Preparation 
This repository contains all the scraping and pre-processing scripts for Tunisian TTS dataset.
1. Download [drejja_to_english_dataset](https://www.kaggle.com/datasets/khawlajlassi/drejja-to-english) from kaggle
2. Install the chromium webdriver 
```bash
pip install selenium
apt-get update # to update ubuntu to correctly run apt install
apt install chromium-chromedriver
cp /usr/lib/chromium-browser/chromedriver /usr/bin
```
3. Scrape data :
```bash
python3 scraping.py \
 --drejja-to-english-metadata-file-path ${THA_PATH_OF_DREJJA_TO_ENGLISH_METADATA_FILE}\
 --save-data-directory-path ${THE_PATH_WHERE_TO_SAVE_THE_DATA}
```
4. Download audios
```bash
python3 download_audios.py \
 --txt-file-path ${SCRAPED_DATA_FILE_PATH}\
 --save-data-directory-path ${THE_PATH_WHERE_TO_SAVE_THE_DOWNLOADED_AUDIOS}
```
5. Extract mono-speaker tunisian dataset
```bash
python3 generate_tunisian_dataset.py \
 --txt-file-path ${SCRAPED_DATA_FILE_PATH}\
 --mp3-files-path ${THE_PATH_OD_THE_DOWNLOADED_AUDIOS}\
 --save-data-directory-path ${THE_PATH_WHERE_TO_SAVE_THE_GENERATED_DATASET}
```


