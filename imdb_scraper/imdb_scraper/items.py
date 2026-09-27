# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import scrapy


class ImdbScraperItem(scrapy.Item):
    # define the fields for your item here like:
    titre = scrapy.Field()
    annee = scrapy.Field()
    duree = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    score = scrapy.Field()
    public = scrapy.Field()
    pays = scrapy.Field()
    acteurs = scrapy.Field()
    

def convert_duration_to_minutes(duration):
    """
    Convertit une durée IMDb (« 2h 22m », « 2h », « 45m ») en nombre de minutes.

    Renvoie None si la durée est absente ou dans un format inconnu.
    """
    if not duration:
        return None
    heures = re.search(r'(\d+)\s*h', duration)
    minutes = re.search(r'(\d+)\s*m', duration)
    if not heures and not minutes:
        return None
    return (int(heures.group(1)) * 60 if heures else 0) + (int(minutes.group(1)) if minutes else 0)


def convertir_score(score):
    """Convertit la note IMDb scrapée (texte, par exemple « 9.3 ») en nombre, ou None si elle est absente."""
    try:
        return float(score)
    except (TypeError, ValueError):
        return None
