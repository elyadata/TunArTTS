Now that you have created your *data* and *downloads* folders, we need to adjust the hyper-parameters by deleting the old version and copying the one that's in this repository:
```bash
rm conf/tuning/finetune_tacotron2.yaml
mv used_scripts/finetune_tacotron2.yaml conf/tuning
```

Delete the ```run.sh``` file and __replace__ it by the one existing in this repository

```bash
rm run.sh
```
Before running we need to execute the following script to downsample our dataset from 44100 Hz to 22050 Hz.
```sh
pip install pydub
python3 used_scripts/downsample.py
```
Moreover, you need to create the metadata for your training by applying the follwing command:
```bash
./run.sh --stage 2 --stop-stage 5
```

### Loading the pre-trained model
download the pre-trained model from this link: [Zenodo model](https://zenodo.org/record/4925105) and load it under the **downloads** folder.
\
\
After <font color="43EEC0"> stage 5</font>, we need to copy the token_list as stated exactly in this [Pre-trained model recipe](https://github.com/espnet/espnet/blob/master/egs2/jvs/tts1/README.md).

### Running until stage 6
Now we are going to start the training.

```sh
 ./run.sh \
    --stage 6 \
    --stop-stage 6 \
    --train_args "--init_param downloads/path/to/.../checkpoint.pth:::tts.enc.embed" \
    --tag finenetune_tacotron2_raw_phn
```
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