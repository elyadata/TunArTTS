Now that you have created your *data* and *downloads* folders, we need to adjust the hyper-parameters by deleting the old version and copying the one that's in this repository:
```bash
rm conf/tuning/train_tacotron2.yaml
mv used_scripts/train_tacotron2.yaml conf/tuning
```

Delete the ```run.sh``` file and __replace__ it by the one existing in this repository

```bash
rm run.sh
```
Finally, all you have to do is to apply the following command to start training your model on your new dataset.
```bash
./run.sh --stage 2
```