# FilmEngine

FilmEngine is an end-to-end Spark based data pipeline that extracts, models and loads data into a Postgres database.

## Background
TrueFilm is a film investment company - they fund new projects, with the goal of taking a share of any profits. In the past, these decisions were made on gut feeling, but as the industry becomes more and more competitive they  would like to become more data driven. They believe that by understanding which films have performed well in the past, they can make better decisions. In order to aid TrueFilm with their decision making process we'll need to source relevant data, model it and extract value out of it. For this exercise we'll be creating an *engine* that consists of various modules to help us make this happen. To understand the process let's discuss the task on hand in three sections; **What** the steps should be, **how** we execute these and **why** we'll be doing it in this manner.

### What
To make data driven decisions we'll need data that gives us flm digests and metadata to drive our calculations. For the first dataset we'll use a Wikimedia extract of the latest films (approx 722MB) and a Kaggle metadata dataset (228MB). An alternative solution is to make use of Wikipedia APIs to extract the relevant metadata.
Conceptually there are a number of functional steps we need to perform to get our insights:
- For each film, calculate the ratio of budget to revenue
- Match each movie in the IMDb dataset with its corresponding Wikipedia page via API or a Wikipedia dump
- Load the top 1000 movies with the highest ratio into a Postgres database, including the following for each movie:
  - Title
  - Budget
  - Revenue
  - Rating
  - Ratio
  - Production
  - Company
  - Wikipedia Page Link
  - Wikipedia Abstract
- Make the process reproducible and automated
### How
Covering all of the key deliverables above we need to develop an "FilmEngine", a reproducible package with modules that support the full data pipeline from data extraction, transformation to loading. The end result is a data model that can be used for drawing insights either via querying it with SQL or by creating data visualizations.
The full data pipeline would consist of the following modules:
1. Extraction
    - Download the key datasets
    - Extract and store the data
2. Transformation
    - Store the data inside Spark DataFrames with inferred Schemas
    - Standardize any facts e.g. dates, integers, varchar
    - Apply business logic
    - Populate the Wikipedia metadata
3. Loading
    - Create the relevant target table in the database
    - Load the DataFrames into the respective tables

Having the above setup we can run the package, perform tests to validate the output and explore the dataset to extract further insights.

### Why
The choice of technology stack is as follows:
- Programming Language: **Python** is the language of choice due the ease of use, a wide range of frameworks available and versatility
- Data Integration: **Apache Spark**, a big data framework that is a high-performing, in-memory framework that facilitates the processing of large volumes of data 
- Storage: **Postgres Database**, a simple, universally adopted relational database for keeping the transformed data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

[Postgres](https://www.enterprisedb.com/postgresql-tutorial-resources-training?cid=47) (12.4)

[Python](https://www.python.org/downloads/) (3.8.5)

[Pip](https://pip.pypa.io/en/stable/installing/#) (20.2.3)

[PySpark](https://pypi.org/project/pyspark/) (3.0.1) - Download and install the Spark Framework

[Kaggle_Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv) - Create an account and download the dataset

[Kaggle_API](https://github.com/Kaggle/kaggle-api) - Install the Kaggle API

### Installing

Bellow are the necessary steps for configuring the environment in order to get a development up and running.

1. Install and setup Python and Pip on your machine

```
1. Install Python on your machine Mac/Windows, see the link in the pre-reqs for a link.
2. Install Pip by running the below commands:
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    For more information around configuration, see the link the section above.
```

2. Create an account on Kaggle and acquire your API keys

```
1. Run the following command to access the Kaggle API using the command line: pip install kaggle (You may need to do pip install --user kaggle on Mac/Linux. This is recommended if problems come up during the installation process.) Follow the authentication steps below and you’ll be able to use the kaggle CLI tool.
2. In order to use the Kaggle’s public API, you must first authenticate using an API token. From the site header, click on your user profile picture, then on “My Account” from the dropdown menu. This will take you to your account settings at https://www.kaggle.com/account. Scroll down to the section of the page labelled API:
    - To create a new token, click on the “Create New API Token” button. This will download a fresh authentication token onto your machine.
    - If you are using the Kaggle CLI tool, the tool will look for this token at ~/.kaggle/kaggle.json on Linux, OSX, and other UNIX-based operating systems, and at C:\Users<Windows-username>.kaggle\kaggle.json on Windows. If the token is not there, an error will be raised. Hence, once you’ve downloaded the token, you should move it from your Downloads folder to this folder.
```

2. Install PySpark on your machine

```
1. PySpark is now available in pypi. To install just run:
    pip install pyspark.
2. In case you encounter any worker issues when running the commands make sure you configure your Spark environment. In your "~/.zshrc" or "~/.bin" set up the following variables. These are dependent on your own machine.
    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-14.jdk/Contents/Home/
    export PYSPARK_PYTHON="/usr/bin/python3"
    export PYSPARK_DRIVER_PYTHON="/usr/bin/python3"
```

3. Install a PostgresSQL database on your local machine. Make sure you take note of your "user", "password", "port_number", "db_name" and update it in the "env_variables.py" files under the "./docs/" folder.

```
1. Downloading the installer
2. Launching the installation
3. Selecting the install location
4. Selecting components
5. Selecting where to store data
6. Setting the user password
7. Selecting the port number
8. Setting locale
9. Review and installation
10. Checking the process
```

All done!

## Running the FilmEngine

After the pre-requisites are met and the initial set up is complete all you need to du is to rune the "filmengine.py".
The script executes the full ETL pipeline from extraction, to applying the transformation logic and finally loading the data.
Below is the high level view of the sections and the expected output for each.

### Extract

The following section extracts a dataset from Kaggle 
and decompresses it in the "/files/" subfolder.

Below is the expected output:

```
 Downloading and decompressing the file from rounakbanik/the-movies-dataset...


...The movies_metadata.csv has been downloaded and extracted in the ./files/ directory.
```

### Transformation

Process the CSV file and apply transformations using Spark.
This happens in a few key steps
1. Building a DataFrame from the CSV

```
Expected output:

 Building a Spark DataFrame and a Temporary view...

                                                                                
 ...the DataFrame has now been built.

+--------------------+-------+----+---------+------+--------------------+--------------------+-------------+---------+
|               title| budget|year|  revenue|rating|               ratio|  production_company|wiki_abstract|wiki_link|
+--------------------+-------+----+---------+------+--------------------+--------------------+-------------+---------+
|The Karate Kid, P...|    113|1986|115103979|   5.9|9.817210576186946E-7|[{'name': 'Columb...|         null|     null|
| Paranormal Activity|  15000|2007|193355800|   5.9|7.757719189183877E-5|[{'name': 'Blumho...|         null|     null|
|           Tarnation|    218|2003|  1162014|   7.5|1.876053128447677...|                  []|         null|     null|
|The Blair Witch P...|  60000|1999|248000000|   6.3|2.419354838709677...|[{'name': 'Artisa...|         null|     null|
|                대호|   5000|2015| 11083449|   7.5|4.511231115873768E-4|[{'name': 'Next E...|         null|     null|
|          Eraserhead|  10000|1977|  7000000|   7.5|0.001428571428571...|[{'name': 'Americ...|         null|     null|
|            猛龍過江| 130000|1972| 85000000|   7.4|0.001529411764705...|[{'name': 'Golden...|         null|     null|
|      Pink Flamingos|  12000|1972|  6000000|   6.2|               0.002|[{'name': 'Dreaml...|         null|     null|
|       Super Size Me|  65000|2004| 28575078|   6.6|0.002274709451361...|[{'name': 'Kathbu...|         null|     null|
|         The Gallows| 100000|2015| 42664410|   4.9|0.002343873968959...|[{'name': 'New Li...|         null|     null|
|          Open Water| 130000|2004| 54667954|   5.3|0.002377992781657788|[{'name': 'Plunge...|         null|     null|
|The Texas Chain S...|  85000|1974| 30859000|   7.1|0.002754463851712...|[{'name': 'New Li...|         null|     null|
|               Bambi| 858000|1942|267447150|   6.8|0.003208110462197...|[{'name': 'Walt D...|         null|     null|
|             Mad Max| 400000|1979|100000000|   6.6|               0.004|[{'name': 'Kenned...|         null|     null|
|           Halloween| 300000|1978| 70000000|   7.4|0.004285714285714286|[{'name': 'Compas...|         null|     null|
|The Legend of Bog...| 100000|1972| 22000000|   5.6|0.004545454545454545|[{'name': 'P & L'...|         null|     null|
| Alice in Wonderland|3000000|1951|572000000|   7.0|0.005244755244755245|[{'name': 'RKO Ra...|         null|     null|
|   American Graffiti| 777000|1973|140000000|   6.9|             0.00555|[{'name': 'Lucasf...|         null|     null|
|   Let's Do It Again|  70000|1975| 11800000|   7.7|0.005932203389830509|[{'name': 'First ...|         null|     null|
|         Blood Feast|  24500|1963|  4000000|   5.3|            0.006125|[{'name': 'Friedm...|         null|     null|
+--------------------+-------+----+---------+------+--------------------+--------------------+-------------+---------+
only showing top 20 rows

```

2. Creating a temporary view, applying the business logic

```
Expected output:

 Now populating the Wikipedia links and abstracts...

Row 0 has been populated for the film: The Karate Kid, Part II
Row 1 has been populated for the film: Paranormal Activity
Row 2 has been populated for the film: Tarnation
Row 3 has been populated for the film: The Blair Witch Project
Row 4 has been populated for the film: 대호
Row 5 has been populated for the film: Eraserhead
Row 6 has been populated for the film: 猛龍過江
Row 7 has been populated for the film: Pink Flamingos
Row 8 has been populated for the film: Super Size Me
Row 9 has been populated for the film: The Gallows
Row 10 has been populated for the film: Open Water
Row 11 has been populated for the film: The Texas Chain Saw Massacre
Row 12 has been populated for the film: Bambi
Row 13 has been populated for the film: Mad Max
Row 14 has been populated for the film: Halloween
Row 15 has been populated for the film: The Legend of Boggy Creek
Row 16 has been populated for the film: Alice in Wonderland
Row 17 has been populated for the film: American Graffiti
Row 18 has been populated for the film: Let's Do It Again
Row 19 has been populated for the film: Blood Feast
Row 20 has been populated for the film: A Ghost Story

 ...links and abstracts populated.
```

3. Populating the Wiki links and abstracts

```
Expected output:

 Loading the final DataFrame into the PostgreSQL DB.

                                                                                
 ...the ETL process is now complete! 

 +--------------------+-------+----+---------+-----------------+--------------------+--------------------+--------------------+--------------------+
|               title| budget|year|  revenue|           rating|               ratio|  production_company|       wiki_abstract|           wiki_link|
+--------------------+-------+----+---------+-----------------+--------------------+--------------------+--------------------+--------------------+
|The Karate Kid, P...|    113|1986|115103979|5.900000095367432|9.817210576186946E-7|[{'name': 'Columb...|The Karate Kid Pa...|https://en.wikipe...|
| Paranormal Activity|  15000|2007|193355800|5.900000095367432|7.757719189183877E-5|[{'name': 'Blumho...|Paranormal Activi...|https://en.wikipe...|
|           Tarnation|    218|2003|  1162014|              7.5|1.876053128447677...|                  []|                null|https://en.wikipe...|
|The Blair Witch P...|  60000|1999|248000000|6.300000190734863|2.419354838709677...|[{'name': 'Artisa...|The Blair Witch P...|https://en.wikipe...|
|                대호|   5000|2015| 11083449|              7.5|4.511231115873768E-4|[{'name': 'Next E...|Ra Mi-ran (born M...|https://en.wikipe...|
|          Eraserhead|  10000|1977|  7000000|              7.5|0.001428571428571...|[{'name': 'Americ...|Eraserhead is a 1...|https://en.wikipe...|
|            猛龍過江| 130000|1972| 85000000|7.400000095367432|0.001529411764705...|[{'name': 'Golden...|The Way of the Dr...|https://en.wikipe...|
|      Pink Flamingos|  12000|1972|  6000000|6.199999809265137|               0.002|[{'name': 'Dreaml...|Pink Flamingos is...|https://en.wikipe...|
|       Super Size Me|  65000|2004| 28575078|6.599999904632568|0.002274709451361...|[{'name': 'Kathbu...|Super Size Me is ...|https://en.wikipe...|
|         The Gallows| 100000|2015| 42664410|4.900000095367432|0.002343873968959...|[{'name': 'New Li...|The Gallows is a ...|https://en.wikipe...|
|          Open Water| 130000|2004| 54667954|5.300000190734863|0.002377992781657788|[{'name': 'Plunge...|Open Water is a 2...|https://en.wikipe...|
|The Texas Chain S...|  85000|1974| 30859000|7.099999904632568|0.002754463851712...|[{'name': 'New Li...|The Texas Chain S...|https://en.wikipe...|
|               Bambi| 858000|1942|267447150|6.800000190734863|0.003208110462197...|[{'name': 'Walt D...|Bambi is a 1942 A...|https://en.wikipe...|
|             Mad Max| 400000|1979|100000000|6.599999904632568|               0.004|[{'name': 'Kenned...|Mad Max is a 1979...|https://en.wikipe...|
|           Halloween| 300000|1978| 70000000|7.400000095367432|0.004285714285714286|[{'name': 'Compas...|Halloween is an A...|https://en.wikipe...|
|The Legend of Bog...| 100000|1972| 22000000|5.599999904632568|0.004545454545454545|[{'name': 'P & L'...|The Legend of Bog...|https://en.wikipe...|
| Alice in Wonderland|3000000|1951|572000000|              7.0|0.005244755244755245|[{'name': 'RKO Ra...|Alice in Wonderla...|https://en.wikipe...|
|   American Graffiti| 777000|1973|140000000|6.900000095367432|             0.00555|[{'name': 'Lucasf...|American Graffiti...|https://en.wikipe...|
|   Let's Do It Again|  70000|1975| 11800000|7.699999809265137|0.005932203389830509|[{'name': 'First ...|Let's Do It Again...|https://en.wikipe...|
|         Blood Feast|  24500|1963|  4000000|5.300000190734863|            0.006125|[{'name': 'Friedm...|Blood Feast is a ...|https://en.wikipe...|
+--------------------+-------+----+---------+-----------------+--------------------+--------------------+--------------------+--------------------+
```
## Tests

To verify the script has worked we can do a series of simple SQL queries to check the following:
- Describe the schema in the DB to make sure all appropriate data types apply.
- Check the count of rows, we're expecting 1000 rows.
- Verify budget and revenue columns for any outliers.
- Check for Nulls in the wiki abstracts, links columns to see if these are valid films titles.

The full set of queries is provided in the "/tests/" folder.

## Roadmap

In the future there are a number of improvements that can be implemented as part of the features roadmap.

Performance upgrades
- As it stands, the filmengine performs a loop over rows to acquire the relevant Wikipedia metadata. This is not exactly efficient, an alternative method would be to create two custom modules to download the whole dump and parse it to extract the values.
- The direct download module is already created under "/modules/deprecated/" but has been taken out for the time being until te parser is complete.
- The parser would be looking at the XML dump and extracting relevant the relevant values and store it in a tabular format.
- This DataFrame would then be joined with the main metadata table within Spark to populate the relevant metadata.

Portability
- As you may have observed, there are a few pre-requisites to be met in order to get up and running. Many times this causes local incompatibilities i.e. "It works on my machine!!"
- In the future the idea is to containerize the script with all the dependencies inside a docker container. This would alleviate any potential incompatibility issues and would make for a trip that's universal across various operating systems; Linux, MacOS or Windows. 

Modularity
- Currently the core of the script is written in Spark and the DataFrames schemas are hardcoded.
- In the future there's space for improvement to create a function that parses the schema of the CSV file and creates the schema based on that. This would make the filmengine a lot more modular, since fewer to no edits would have to be done to the core of the script other than point to the right download links.

## Contributing

For this project contribution is not allowed, therefore there is no need for details on code of conduct, and the process for submitting pull requests.

## Versioning

Versioning is not implemented. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Alexander Sommer** - *Initial work* - [salexommer](https://github.com/salexommer)


## License

This project is is not licensed and is free to use.
