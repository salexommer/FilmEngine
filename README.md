# FilmEngine

FilmEngine is an end-to-end Spark based data pipeline that extracts, models and loads data into a Postgres database.

## Background
TrueFilm is a film investment company - they fund new projects, with the goal of taking a share of any profits. In the past, these decisions were made on gut feeling, but as the industry becomes more and more competitive they  would like to become more data driven. They believe that by understanding which films have performed well in the past, they can make better decisions. In order to aid TrueFilm with their decision making process we'll need to source relevant data, model it and extract value out of it. For this exercise we'll be creating an *engine* that consists of various modules to help us make this happen. To understand the process let's discuss the task on hand in three sections; **What** the steps should be, **how** we execute these and **why** we'll be doing it in this manner.

### What
To make data driven decisions we'll need data that gives us flm digests and metadata to drive our calculations. For the first dataset we'll use a Wikimedia extract of the latest films (approx 722MB) and a Kaggle metadata dataset (228MB).
Conceptually there are a number of functional steps we need to perform to get our insights:
- For each film, calculate the ratio of budget to revenue
- Match each movie in the IMDb dataset with its corresponding Wikipedia page
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

[PySpark](https://pypi.org/project/pyspark/) (3.0.1)

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Contributing

For this project contribution is not allowed, therefore there is no need for details on code of conduct, and the process for submitting pull requests.

## Versioning

Versioning is not implemented. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Alexander Sommer** - *Initial work* - [salexommer](https://github.com/salexommer)


## License

This project is is not licensed and is free to use.

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc