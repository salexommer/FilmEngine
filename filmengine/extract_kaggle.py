# Initial filmengine script that will be split into separate modules later
from kaggle.api.kaggle_api_extended import KaggleApi
import fnmatch
import os
import zipfile

# Variables and prep
api = KaggleApi()
api.authenticate()
kaggle_dataset = 'rounakbanik/the-movies-dataset'
kaggle_file_name = 'movies_metadata.csv'

 #Download all files of a dataset
# Signature: dataset_download_files(dataset, path=None, force=False, quiet=True, unzip=False)
#api.dataset_download_files('avenn98/world-of-warcraft-demographics')

# Download single file
#Signature: dataset_download_file(dataset, file_name, path=None, force=False, quiet=True)
api.dataset_download_file(kaggle_dataset,kaggle_file_name,path='./files/')

# Get the name of the downloaded archive)
for file in os.listdir('./files/'):
    if fnmatch.fnmatch(file, '*' + kaggle_file_name + '*'):
        print(file)
        kaggle_archive_name = file

# Decompress
with zipfile.ZipFile("./files/" + kaggle_archive_name, 'r') as zip_ref:
    zip_ref.extractall('./files/')

print("The file " + kaggle_file_name + " has been decompressed")