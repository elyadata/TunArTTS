#!/bin/bash

echo "dataset_directory_absolute_path: $1";
echo "manifest_directory_path: $2";
echo "alphabet: $3";
echo "relative_path_to_wav_folder_in_dataset_inside_downloads: $4"
echo "train_yaml_path: $5";


if [ $# -ne 5 ]; then
  echo "Usage: $0 <dataset_directory_absolute_path> <manifest_directory_path> "
  echo  "     <dataset_directory_absolute_path>    : path to the directory where to save data"
  echo  "     <manifest_directory_path>  : path to the directory where to save tsv files"
  echo  "     <alphabet> : the alphabet, ar for arabic, bw for buckwalter or phn for phonemes"
  echo  "     <wav_folder_path>  : relative path to wav folder in dataset inside downloads"
  echo  "     <train_yaml_path> : path of the train.yaml file"
  exit 1
fi


./settings.sh $1

if [[ "$3" == "phn" ]]
then
  python3  ../../dataset_recreation/arabic_to_phonemes.py --data-root $1
  g2p=none
  type=phn
elif [[ "$3" == "bw" ]]
then
  python3 ../../dataset_recreation/arabic_to_buckwalter.py --dataset-dir-path $1
  g2p=none
  type=char
else
  g2p=espeak_ng_arabic
  type=char
fi

#To split the dataset, and generate tsv file for each split
python3 ../../dataset_recreation/split_dataset.py \
 --data-root $1 \
 --output-manifest-root $2 \
 --alphabet $3

#To generate kaldi-style data directory
SAVE_DATA_DIRECTORY_PATH=espnet/egs2/qasr_tts/tts1/data
python3 ../tools/data_dir_generation.py \
 --tsv-files-path $2 \
 --save-data-directory-path ${SAVE_DATA_DIRECTORY_PATH}

cd espnet/egs2/qasr_tts/tts1

#Update the hyperparameters
rm conf/tuning/finetune_tacotron2.yaml
cp $5 conf/tuning

#To sort the generated files of the data directory
utils/fix_data_dir.sh data/test
utils/fix_data_dir.sh data/dev
utils/fix_data_dir.sh data/train

pip install pydub
python3 downsample.py $4

./run.sh --stage 2 \
 --stop-stage 5 \
 --fs 22050 \
 --cleaner none \
 --token_type "${type}"\
 --g2p "${g2p}" \
 --train_set train \
 --valid_set dev \
 --test_sets test \
 --srctexts "data/train/text"