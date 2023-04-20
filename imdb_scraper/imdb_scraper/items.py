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
    

def convert_duration_to_minutes(duration):
    hours, minutes = duration.split('h ')
    hours = int(hours)
    minutes = int(minutes[:-1])
    total_minutes = hours * 60 + minutes
    return total_minutes