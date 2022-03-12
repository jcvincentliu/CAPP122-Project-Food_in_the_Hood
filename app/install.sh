#!/bin/bash

# 1. Create Virtual environment
echo -e "1. Creating new virtual environment..."

# Remove the env directory if it exists
if [[ -d env ]]; then
    echo -e "\t--Virtual Environment already exists. Deleting old one now."
    rm -rf env
fi

python3 -m venv env

if [[ ! -d env ]]; then
    echo -e "\t--Could not create virutal environment...Please make sure venv is installed"
    exit 1
fi

# 4. Install Requirements

echo -e "4. Installing Requirements..."
if [[ ! -e "requirements.txt" ]]; then
    echo -e "\t--Need to requirements.txt to install packages."
    exit 1
fi

source env/bin/activate
pip install -r requirements.txt