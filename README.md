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

### **Why**

