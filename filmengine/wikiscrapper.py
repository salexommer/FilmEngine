# wikiscrapper.py
import wikipedia

def wikiscrap(i):
    summary = print(wikipedia.summary(i +" (Movie)"))
    link = wikipedia.page(i +" (Movie)").url
    return summary
    return link

wikiscrap("Bambi")