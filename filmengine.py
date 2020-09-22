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
import wikipedia
import pandas as pd

# Own Modules

