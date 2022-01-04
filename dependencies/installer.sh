#!/usr/bin/env bash
#
echo "Setting up model dependencies...."

apt-get update && apt-get upgrade -y
apt-get install -y sudo wget python3-pip git

apt install python-is-python3
git clone https://github.com/Open-Speech-EkStep/vakyansh-tts
cd vakyansh-tts
pip3 install --no-cache-dir -r requirement.txt
bash install.sh
python3 setup.py bdist_wheel
pip install -e .
cd tts_infer
mkdir -p translit_models
#gsutil -m cp -r gs://vakyaansh-open-models/translit_models .


