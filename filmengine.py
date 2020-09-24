'''
Description
-----------
The FilmEngine is an end-to-end ETL pipeline that processes data from Kaggle,
applies business transformations with Spark and loads it into a PostgreSQL DB.

Author: Alexander Sommer
Initial Release: 20/09/2020
'''


# Built-in Libraries
import os
import zipfile
import fnmatch

# Other Libraries
import wikipedia
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, lit, udf
from kaggle.api.kaggle_api_extended import KaggleApi

# Own Modules
from modules.kaggle_extractor import download_kaggle, decompress_kaggle
from docs.env_variables import database, tgt_table, user, password, jdbcUrl, jdbcDriver
from modules.wiki_scraper import wikilink, wikiabstract

# Variables
kaggle_dataset = 'rounakbanik/the-movies-dataset'
kaggle_file_name = 'movies_metadata.csv'
files_dir = './files/'


"""
Extract
--------
The following section extracts a dataset from Kaggle 
and decompresses it in the "/files/" subfolder.

"""

# Initiate the Spark engine
spark = SparkSession \
    .builder \
    .appName("FilmEngine") \
    .config("spark.jars", "./docs/postgresql-42.2.16.jar") \
    .getOrCreate()
sc = spark.sparkContext.getOrCreate()

# Download and extract the kaggle metadata file
print("\n Downloading and decompressing the file from " + kaggle_dataset + "...\n")
download_kaggle(kaggle_dataset,kaggle_file_name,files_dir)
decompress_kaggle(kaggle_file_name, files_dir)
print("\n...The " + kaggle_file_name + " has been downloaded and extracted in the " + files_dir + " directory.\n")


"""
Transform
---------
Process the CSV file and apply transformations using Spark.
This happens in a few key steps
1. Building a DataFrame from the CSV
2. Creating a temporary view, applying the business logic
3. Populating the Wiki links and abstracts

"""

# Build a DataFrame from the CSV file
print("\n Building a Spark DataFrame and a Temporary view" + "...\n")
df = spark.read \
    .option('header', 'true') \
        .csv(files_dir + kaggle_file_name)
df2 = df.select(df["original_title"].cast('string').alias("title"),\
    df["budget"].cast('integer').alias("budget"),
    df["release_date"].cast('date').alias("release_date"),
    df["revenue"].cast('integer').alias("revenue"),
    df["vote_average"].cast('float').alias("rating"),
    df["production_companies"].cast('string').alias("production_company"))

# Create a temporary view, applying calculations and adding new columns
df2.createOrReplaceTempView("metadata")
sqlDF = spark.sql(
    "SELECT \
        title, \
        budget, \
        year(release_date) as year, \
        revenue, \
        rating, \
        budget/revenue as ratio, \
        production_company \
    FROM \
        metadata\
    WHERE \
        revenue IS NOT NULL\
        AND revenue != 0\
        AND budget != 0\
        AND rating IS NOT NULL\
        AND budget > 10\
    ORDER BY ratio asc\
    LIMIT 1000"
    )
sqlDF = sqlDF.select("*")\
    .withColumn("wiki_abstract",lit(None).cast('string'))\
    .withColumn("wiki_link",lit(None).cast('string'))
sqlPDF = sqlDF.select("*").toPandas()
print("\n ...the DataFrame has now been built.\n")
sqlDF.show()

# Populate the DataFrame with Wikipedia links and abstracts
print("\n Now populating the Wikipedia links and abstracts...\n")
m = 0
while m <= 1000:
    func_val = sqlPDF.at[m, 'title']
    link = wikilink(func_val)
    abstract = wikiabstract(func_val)
    sqlPDF.at[m, 'wiki_link'] = link
    sqlPDF.at[m, 'wiki_abstract'] = abstract
    print("Row " + str(m) + " has been populated for the film: " + func_val)
    m = m + 1
sqlDF = spark.createDataFrame(sqlPDF)
print("\n ...links and abstracts populated.\n")

"""
Load
----
Finally, load the final DataFrame into a PostgreSQL DB.
This is the final step in the process.
"""

print("\n Loading the final DataFrame into the PostgreSQL DB.\n")
sqlDF.select("title","budget", "year", "revenue", "ratio", "production_company", "wiki_link", "wiki_abstract") \
    .write.format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbcUrl) \
    .option("dbtable", tgt_table) \
    .option("user", user) \
    .option("password", password) \
    .option("driver", jdbcDriver) \
    .save()
sqlDF.show()
print("\n ...the ETL process is now complete! \n")
