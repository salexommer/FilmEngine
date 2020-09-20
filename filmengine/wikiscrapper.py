# wikiscrapper.py
import wikipedia

def wikiscrap(i):
    print(wikipedia.summary(i +" (Movie)"))
    print(wikipedia.page(i +" (Movie)").url)

wikiscrap("Bambi")