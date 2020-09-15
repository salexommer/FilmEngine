# Import PySpark to perform data transformations
from pyspark.sql import SparkSession

# Initiate the Spark engine
spark = SparkSession \
    .builder \
    .appName("FilmEngine") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc = spark.sparkContext.getOrCreate()