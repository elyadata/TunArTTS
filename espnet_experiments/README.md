Through our experiments we have compared, mainly, two resulted systems: 
- Running an experiment from scratch on TunArTTS.
- Applying Transfer Learning on TunArTTS using the English dataset LJSPeech.

Using this repository, the steps in common to follow for both approaches are:
- The installation of ESPnet.
- The creation of the __downloads__ folder containing the dataset.
- The creation of the __data__ folder containing the subdivision of your train/dev/test sets conforming with the sets chosen in our experiments. 

Eventually, both methods diverge in their training.
## ESPnet Installation
For both methods you'll need to run a script to guarantee the installation of ESPnet on your machine.
```bash
run.sh
```
If you are going to run the __Running from scratch__ experiment, you need to use the __LJSpeech__ recipe by visiting the following branch. 
```bash
espnet/egs2/ljspeech/tts1
```
Otherwise, if you are running the __Transfer Learning__ experiment on English, you need to use the __qasr__ experiment by following this branch.
```bash
espnet/egs2/qasr_tts/tts1
```

## Downloads folder
Put the dataset (TunArTTS)'s absolute path as a parameter and the script will displace it under a newely created folder entitled *downloads* and in it put a another folder entitled *dataset-tun* that contains another folder named *wav* containing your .wav audio files.
So the finale tree branch would be:
```bash
├───tts1
    └───downloads
        └───wav
            └───***.wav file
            └───***.wav file
            └───...
```

## Data folder
Now to create another folder under the name of *data* where we are going to put the subdivisions of our sets for ESPnet to access each partition's set of files. Another step that the script will take care of.