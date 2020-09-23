'''
The FilmEngine is an end-to-end ETL pipeline that processes data from Kaggle,
applies business transformations with Spark and loads it into a PostgreSQL DB.

Author: Alexander Sommer
Initial Release: 20/09/2020
'''

# Built-in Libraries
import fnmatch
import os
import zipfile

# Other Libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, lit, udf
from kaggle.api.kaggle_api_extended import KaggleApi
import wikipedia
import pandas as pd

# Own Modules
from filmengine.kaggle_extract 
# Variables
kaggle_dataset = 'rounakbanik/the-movies-dataset'
kaggle_file_name = 'movies_metadata.csv'
files_dir = './files/'

# Extract: Download and extract the kaggle metadata file
