# FilmEngine
## Challenge description
TrueFilm is a film investment company - they fund new projects, with the goal of taking a share of any profits. In the past, these decisions were made on gut feeling, but as the industry becomes more and more competitive they  would like to become more data driven. They believe that by understanding which films have performed well in the past, they can make better decisions.

## Chosen Approach
In order to aid TrueFilm with their decision making process we'll need to source relevant data, model it and extract value out of it. For this exercise we'll be creating an *engine* that consists of various modules to help us make this happen. To understand the process let's discuss the task on hand in three sections; **What** the steps should be, **how** we execute these and **why** we'll be doing it in this manner.

### **What**
To make data driven decisions we'll need data that gives us flm digests and metadata to drive our calculations. For the first dataset we'll use a Wikimedia extract of the latest films (approx 722MB) and a Kaggle metadata dataset (228MB).
Conceptually there are a number of functional steps we need to perform to get our insights:
- For each film, calculate the ratio of budget to revenue
- Match each movie in the IMDB dataset with its corresponding Wikipedia page
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
### **How**
Covering all of the key deliverables above we need to develop an "FilmEngine", a reproducible package with modules that support the full data pipeline from data extraction, transformation to loading. The end result is a data model that can be used for drawing insights either via querying it with SQL or by creating data visualizations.
The full data pipeline would consist of the following modules:
1. Configuration
    - Postgres Database
    - Python 3.x + Dependencies
    - PySpark
2. Extraction
    - Download the key datasets
    - Extract and store the data
3. Transformation
    - Store the data inside Spark DataFrames with inferred Schemas
    - Standardize any facts e.g. dates, integers, varchar
    - Apply business logic
4. Loading
    - Create the relevant target table in the database
    - Load the DataFrames into the respective tables
Having the above setup we can run the package, perform tests to validate the output and explore the dataset to extract further insights.
### **Why**
The choice of technology stack is as follows:
- Programming Language: **Python** is the language of choice due the ease of use, a wide range of frameworks available and versatility
- Data Integration: **Apache Spark**, a big data framework that is a high-performing, in-memory framework that facilitates the processing of large volumes of data 
- Storage: **Postgres Database**, a simple, universally adopted relational database for keeping the transformed data
