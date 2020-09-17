# Initial filmengine script that will be split into separate modules later
from pyspark.sql import SparkSession
from pyspark.sql import DataFrameReader
import os

# Initiate the Spark engine
spark = SparkSession \
    .builder \
    .appName("FilmEngine") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc = spark.sparkContext.getOrCreate()

# Export Spark environment variables
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/bin/python3'

#df = spark.read.csv(path='./files/movies_metadata.csv',header=True,inferSchema=True)

#df.show()
#df2 = df.first()
#df2.show()


#df = spark.read.format("csv").option("header", 'true').option("delimiter", ",").load('./files/movies_metadata.csv')
#df.show()

data=sc.textFile('./files/movies_metadata.csv')
firstRow=data.first()
data=data.filter(lambda row: row != firstRow)
#df = spark.read.csv(data,header=True)
df = spark.read.format("csv").option("header", 'true').option("delimiter", ",").load(data)
df.show()
