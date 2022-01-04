#!/usr/bin/env bash
#
echo "Setting up model dependencies...."

apt-get update && apt-get upgrade -y
apt-get install -y sudo wget python3-pip git


git clone https://github.com/Open-Speech-EkStep/vakyansh-tts
pip3 install --no-cache-dir -r requirement.txt
cd vakyansh-tts
bash install.sh
python setup.py bdist_wheel
pip install -e .
cd tts_infer
gsutil -m cp -r gs://vakyaansh-open-models/translit_models .

apt install python-is-python3
