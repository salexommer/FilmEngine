'''
This test file provides a number of tests to be run on the table in the DB.

Author: Alexander Sommer
Initial Release: 20/09/2020
'''

select * from film_metadata;

-- Describe the schema in the DB to make sure all appropriate data types apply.
SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'film_metadata';

-- Check the count of rows, we're expecting 1000 rows.
SELECT 
	COUNT (*) 
FROM
	film_metadata;
-- Verify year, budget and revenue columns for any outliers.
WITH film_count AS (
  SELECT
    title,
    COUNT(1) AS VALUE
  FROM film_metadata
  GROUP BY 1
), title_count_with_pct AS (
  SELECT
    title,
    value,
    value / (AVG(value) OVER ()) AS pct_of_mean
  FROM film_count
  ORDER BY 1
)
SELECT 
	* 
FROM 
	title_count_with_pct
WHERE 
	pct_of_mean >= 1.0;

-- Check for Nulls in the wiki abstracts, links columns to see if these are valid films titles.
SELECT 
	title
FROM
	film_metadata
WHERE
	wiki_link IS NULL
OR
	wiki_abstract IS NULL;