#!/usr/bin/env bash
#
echo "Setting up model dependencies...."

apt-get update && apt-get upgrade -y
apt-get install -y sudo wget python3-pip git libsndfile1 libsndfile1-dev

apt install python-is-python3
git clone https://github.com/Open-Speech-EkStep/vakyansh-tts -b dev
cd vakyansh-tts
pip3 install --no-cache-dir -r requirements.txt
bash install.sh
python3 setup.py bdist_wheel
pip3 install -e .
pip3 install torch==1.7.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html
cd tts_infer
mkdir -p translit_models
#gsutil -m cp -r gs://vakyaansh-open-models/translit_models .


