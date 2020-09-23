'''
This module creates custom functions to extract links and abstracts from Wikipedia

Author: Alexander Sommer
Initial Release: 20/09/2020
'''

# Other Libraries
import wikipedia

# Provide a Wikipedia link for a movie title
def wikilink(film_title):
    try:
        link = wikipedia.page(film_title +" (Film)").url
        return link
    except:
        return None

# Provide a Wikipedia abstract for a movie title
def wikiabstract(film_title):
    try:
        abstract = wikipedia.summary(film_title +" (Film)")
        return abstract
    except:
        return None