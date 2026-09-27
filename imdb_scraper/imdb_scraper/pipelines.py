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
        # cherche le fichier .env dans le dossier du projet, puis dans ses dossiers parents
        load_dotenv()
        ATLAS_KEY = os.getenv('ATLAS_KEY')
        if not ATLAS_KEY:
            # sans clé, MongoClient se connecterait silencieusement à un MongoDB local
            raise ValueError("Variable ATLAS_KEY absente : ajoutez-la dans le fichier .env à la racine du projet")
        self.client = pymongo.MongoClient(ATLAS_KEY)
        self.db_film = self.client['myfilms']

    def open_spider(self, spider):
        # chaque spider enregistre dans sa propre collection : films et séries ne sont pas mélangés
        self.collection = self.db_film[spider.collection_mongo]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
