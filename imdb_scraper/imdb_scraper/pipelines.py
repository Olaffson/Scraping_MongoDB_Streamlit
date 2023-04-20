# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from dotenv import load_dotenv
import os


class ImdbScraperPipeline:

    def __init__(self) -> None:
        load_dotenv(dotenv_path='/home/apprenant/Documents/Projets/imdb/.env')
        ATLAS_KEY = os.getenv('ATLAS_KEY')
        self.client = pymongo.MongoClient(ATLAS_KEY)
        self.db_film = self.client['myfilms']
        self.collection = self.db_film['film_table']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
