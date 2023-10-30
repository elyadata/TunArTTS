Now that you have chosen to try out the __Running From Scratch__ experiment on TunArTTS, we need to adjust the hyper-parameters by deleting the old version of the parameters file of Tacotron2 model, and copying the one that's in this repository. 

You need to provide the path to ```train_tacotron2.yaml``` so it would be copied to its right place.:
```bash
./run.sh <dataset_directory_absolute_path> <path_where_to_save_tsv_files> <alphabet> <path_to_train_tacotron2.yaml>

```

Finally, your folders will be created along with the splitting of the dataset to test/dev/train subsets and the training will start.
