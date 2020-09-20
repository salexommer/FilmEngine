# Initial filmengine script that will be split into separate modules later
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id 
from pyspark.sql.functions import lit
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
import wikipedia

# Initiate the Spark engine
spark = SparkSession \
    .builder \
    .appName("FilmEngine") \
    .getOrCreate()
sc = spark.sparkContext.getOrCreate()

# Create a UDF for looking up wikipedia links
def wiki_link(v):
    print(wikipedia.page(v + " (Movie)").url)
spark.udf.register("wikiLink", wiki_link)

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
    .withColumn("row_number", monotonically_increasing_id())\
    .withColumn("wiki_abstract",lit(None).cast('string'))\
    .withColumn("wiki_link",lit(None).cast('string'))
sqlDF.createOrReplaceTempView("metadata_wiki")

sqlDF = spark.sql(
    "SELECT \
        title,\
        wikiLink(title) as link\
    FROM\
        metadata_wiki"
)
sqlDF.show()