#!/bin/bash -ue

python3 -m venv venv
source venv/bin/activate
python -m spacy download en
python -m spacy download en_core_web_sm
pip install -r requirements.txt
