import scrapy


class NewsSinaSpider(scrapy.Spider):
    name = 'news.sina'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/']

    def parse(self, response):
        pass
