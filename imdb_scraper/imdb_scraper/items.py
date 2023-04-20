# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

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
    

# def convert_duration_to_minutes(duration):
#     hours, minutes = duration.split('h ')
#     hours = int(hours)
#     minutes = int(minutes[:-1])
#     total_minutes = hours * 60 + minutes
#     return total_minutes


# Fonction pour convertir la durée en minutes
def convert_duration_to_minutes(durée):
    if 'h' in durée and 'm' in durée:
        heure, minute = durée.split("h ")
        heure = int(heure)
        minute = int(minute.replace("m", ""))
    elif 'h' in durée:
        heure = int(durée.replace("h", ""))
        minute = 0
    elif 'm' in durée:
        heure = 0
        minute = int(durée.replace("m", ""))
    else:
        raise ValueError()
    duree_minutes = heure * 60 + minute
    return duree_minutes