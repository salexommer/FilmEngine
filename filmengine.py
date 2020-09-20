# Initial filmengine script that will be split into separate modules later
from pyspark.sql import SparkSession
from pyspark.sql import DataFrameReader
import os

# Initiate the Spark engine
spark = SparkSession \
    .builder \
    .appName("FilmEngine") \
    .getOrCreate()
sc = spark.sparkContext.getOrCreate()

# Build a DataFrame from the CSV file
df = spark.read \
    .option('header', 'true') \
        .csv('./files/movies_metadata.csv')
#df.show()
#df.printSchema()
df.createOrReplaceTempView("metadata")
sqlDF = spark.sql("describe metadata")
sqlDF.show()
sqlDF = spark.sql("SELECT * FROM metadata")
sqlDF.show()
