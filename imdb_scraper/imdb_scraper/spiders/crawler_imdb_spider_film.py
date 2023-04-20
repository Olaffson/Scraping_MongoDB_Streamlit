import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv
from ..items import ImdbScraperItem, convert_duration_to_minutes


class CrawlerImdbSpiderFilm(CrawlSpider):
    name = "crawler_imdb_spider_film"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["http://www.imdb.com/"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback="parse", follow=False),)

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    def parse(self, response):
        
        items = ImdbScraperItem()
        
        annee = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()").get()
        duree = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]/text()").get()
        duree = convert_duration_to_minutes(duree)
        description = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[3]/text()").get()
        # genre = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a/span/text()").get()
        genre = list(set(response.xpath("//main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a/span/text()").getall()))
        score = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]/text()").get()
        public = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a/text()").get()
        pays = response.xpath("//section[@class='ipc-page-section ipc-page-section--base celwidget']/div[2]/ul/li[2]/div/ul/li/a/text()").get()
        acteurs = list(set(response.xpath("//main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li/a/text()").getall()))
        titre = response.xpath("//main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()").get()

        items['acteurs'] = acteurs
        items['pays'] = pays
        items['public'] = public
        items['score'] = score
        items['genre'] = genre
        items['description'] = description
        items['duree'] = duree
        items['annee'] = annee
        items['titre'] = titre

        yield items