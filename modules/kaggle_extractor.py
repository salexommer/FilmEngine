'''
This module provides a function for downloading files from kaggle and decompressing them

Author: Alexander Sommer
Initial Release: 20/09/2020
'''

# Built-in Libraries
import fnmatch
import os
import zipfile

# Other Libraries
from kaggle.api.kaggle_api_extended import KaggleApi

# Download a single file from a dataset
def download_kaggle (kaggle_dataset, kaggle_file_name, files_dir): 
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file(kaggle_dataset,kaggle_file_name,path=files_dir)

# Decompress the archive
def decompress_kaggle (kaggle_file_name, files_dir):
    try:
        for file in os.listdir(files_dir):
            if fnmatch.fnmatch(file, '*' + kaggle_file_name + '*'):
                with zipfile.ZipFile(files_dir + file, 'r') as zip_ref:
                    zip_ref.extractall(files_dir)
    except:
        return None