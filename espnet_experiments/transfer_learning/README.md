Now that you have chosen to try out the __Transfer_Learning__ experiment on TunArTTS, we need to adjust the hyper-parameters by deleting the old version of the parameters file of Tacotron2 model, and copying the one that's in this repository. 

Before running we need to be aware that the following script will downsample our dataset from 44100 Hz to 22050 Hz to match that of LJSpech's.

Moreover, you need to create the metadata for your training by applying the follwing command:
```bash
./run.sh <dataset_directory_absolute_path> <path_where_to_save_tsv_files> <alphabet> <relative_path_to_wav_folder_in_dataset_inside_downloads> <path_to_train_tacotron2.yaml>
```

P.S.
- This path <path_to_train_tacotron2.yaml> must be an absolute path.
- To execute this script, your current position must be under 'espnet_experiments/running_from_scratch'.


### Loading the pre-trained model
Go to `espnet/egs2/qasr_tts/tts1`. Then download the pre-trained model from this link: [Zenodo model](https://zenodo.org/record/4925105), extract it, and load it under the **downloads** folder.
\
P.S. If **downloads** folder does not exist, please create it.
\
\
After <font color="43EEC0"> stage 5</font>, we need to copy the token_list as stated exactly in this [Pre-trained model recipe](https://github.com/espnet/espnet/blob/master/egs2/jvs/tts1/README.md).

### Running only stage 6
Now we are going to start the training.

```sh
 ./run.sh \
    --stage 6 \
    --stop-stage 6 \
    --train_args "--init_param downloads/path/to/.../checkpoint.pth:::tts.enc.embed" \
    --tag finenetune_tacotron2_raw_phn \
    --fs 22050 \
    --cleaner none \
    --token_type char\
    --g2p none \
    --train_set train \
    --valid_set dev \
    --test_sets test \
    --srctexts "data/train/text"
```
<font color="#FF5733"> /!\ Don't forget to replace the __/path/to__ with your pre-trained model checkpoint path inside _downloads_ /!\ </font>

## Run the teacher model on FastSpeech 2.
Run the following command to create the ``durations`` for FastSpeech 2 to train on. 
```sh
 ./run.sh --stage 7 \
    --tts_exp exp/finenetune_tacotron2_raw_phn \
    --inference_args "--use_teacher_forcing true" \
    --test_sets "tr_no_dev dev eval1"
```
Then to run the FastSpeech 2 model
```sh
./run.sh --stage 5 \
    --teacher_dumpdir exp/finenetune_tacotron2_raw_phn/decode_use_teacher_forcingtrue_train.loss.ave \
    --tts_stats_dir exp/finenetune_tacotron2_raw_phn/decode_use_teacher_forcingtrue_train.loss.ave/stats \
    --write_collected_feats true
```