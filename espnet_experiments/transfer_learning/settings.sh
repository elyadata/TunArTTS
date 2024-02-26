#!/bin/bash

ln -s $1 .
#To install espnet
git clone https://github.com/espnet/espnet.git
cd espnet/tools
git clone https://github.com/kaldi-asr/kaldi.git
cd ../..

#To install dependencies
pip install -e espnet

#To create soft links
ln -s $1 espnet/egs2/qasr_tts/tts1
