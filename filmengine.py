# Initial filmengine script that will be split into separate modules later
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id 
from pyspark.sql.functions import lit
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
import wikipedia
import pandas as pd

# Initiate the Spark engine
spark = SparkSession \
    .builder \
    .appName("FilmEngine") \
    .getOrCreate()
sc = spark.sparkContext.getOrCreate()

# Create a UDF for looking up wikipedia links
def wikilink(i):
    try:
        link = wikipedia.page(i +" (Film)").url
        return link
    except:
        return None
def wikiabstract(i):
    try:
        abstract = wikipedia.summary(i +" (Movie)")
        return abstract
    except:
        return None

# Build a DataFrame from the CSV file
df = spark.read \
    .option('header', 'true') \
        .csv('./files/movies_metadata.csv')
df2 = df.select(df["original_title"].cast('string').alias("title"),\
    df["budget"].cast('integer').alias("budget"),
    df["release_date"].cast('date').alias("release_date"),
    df["revenue"].cast('integer').alias("revenue"),
    df["vote_average"].cast('float').alias("rating"),
    df["production_companies"].cast('string').alias("production_company"))

# Create a "working" table, applying calculations and adding new columns
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

# Create a loop to populate the Wiki links and abstracts

m = 0
while m <= 5:
    func_val = sqlPDF.at[m, 'title']
    link = wikilink(func_val)
    abstract = wikiabstract(func_val)
    sqlPDF.at[m, 'wiki_link'] = link
    sqlPDF.at[m, 'wiki_abstract'] = abstract
    print("Row " + str(m) + " has been populated for the film: " + func_val)
    m = m + 1
print("The links and abstracts have been populated.")

# Show the results
sqlDF = spark.createDataFrame(sqlPDF)
sqlDF.repartition(1).write.csv('./files/metadata_sample.csv', header=True,)
sqlDF.show()
