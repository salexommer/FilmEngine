'''
This module provides the necessary environment variables

Author: Alexander Sommer
Initial Release: 20/09/2020
'''

# DB Variables
database = "postgres"
tgt_table = "public.film_metadata"
user = "postgres"
password  = "London.2021"
jdbcUrl = f"jdbc:postgresql://localhost:5432/{database}"
jdbcDriver = "org.postgresql.Driver"

