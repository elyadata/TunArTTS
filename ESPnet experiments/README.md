Through our experiments we have compared, mainly, two resulted systems: 
- Running an experiment from scratch on TunArTTS.
- Applying Transfer Learning on TunArTTS using the English dataset LSPeech.

Using this repository, there steps in common to follow for both steps which are:
- The installation of ESPnet.
- The creation of the __downloads__ folder containing the dataset.
- The creation of the __data__ folder containing the subdivision of your train/dev/test sets conforming with the sets chosen in our experiments. 

## ESPnet Installation
Run the following script would guarantee the installation of ESPnet on your machine.
```bash
./setup.sh
```
If you are going to run the __Running from scratch__ experiment, you need to use the __LJSpeech__ recipe by executing the following command. 
```bash
cd espnet/egs2/ljspeech/tts1
```
Otherwise, if you are running the __Transfer Learning__ experiment on English, you need to use the __qasr__ experiment by executing the following command.
```bash
cd espnet/egs2/qasr_tts/tts1
```

## Downloads folder
Put the dataset (TunArTTS) under a newely created folder entitled *downloads* and in it put a another folder entitled *dataset-tun* that contains another folder named *wav* containing your .wav audio files.
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
Now to create another folder under the name of *data* where we are going to put the subdivisions of our sets for ESPnet to access each partition's set of files. 

Just copy the following __data__ folder attached in this repository to create similar results to ours.