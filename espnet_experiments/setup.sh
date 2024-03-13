#!/bin/bash

#cloning ESPnet
git clone https://github.com/espnet/espnet.git
cd espnet/tools
#cloning kaldi
clone https://github.com/kaldi-asr/kaldi.git
#settling the setup
./setup_python.sh $(command -v python3)
cd ../..
pip install -e 'espnet'
