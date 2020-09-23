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

# Variables and prep
kaggle_dataset = 'rounakbanik/the-movies-dataset'
kaggle_file_name = 'movies_metadata.csv'
files_dir = './files/'

# Download single file
def download_kaggle (kaggle_dataset, kaggle_file_name, files_dir): 
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file(kaggle_dataset,kaggle_file_name,path=files_dir)

# Get the name of the downloaded archive)
def decompress_kaggle (kaggle_file_name, kaggle_archive_name, files_dir):
    for file in os.listdir(files_dir):
        if fnmatch.fnmatch(file, '*' + kaggle_file_name + '*'):
            kaggle_archive_name = file
            with zipfile.ZipFile(files_dir + kaggle_archive_name, 'r') as zip_ref:
                zip_ref.extractall(files_dir)