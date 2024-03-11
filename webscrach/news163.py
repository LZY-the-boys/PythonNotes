import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from news.items import NewsItem

## 要先在items.py中定义items中以下几个属性：news_thread、news_title、news_time、news_source、
## source_url、news_body

class News163Spider(CrawlSpider):
    name = 'news163'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://news.163.com/20/0622/\d+/.*/?\.html'), callback='parse_item', follow=True),
    ) ## 此处的正则表达式中，200622代表本人爬取的是2020年6月22日的数据，具体操作请F12查看新闻URL对应更改

    def parse_item(self, response):
        item = NewsItem()
        item['news_thread'] = response.url.strip().split('.')[-2].split('/')[-1]

        self.get_title(response, item)
        self.get_time(response, item)
        self.get_source(response, item)
        self.get_source_url(response, item)
        self.get_text(response,item)
        self.write_to_txt(item)
        return item

    def get_title(self, response, item):
        title = response.css('.post_content_main h1::text').extract()  #extract()之后是一个列表
        if title:  ## 防止空标题
            item['news_title'] = title[0]

    def get_time(self, response, item):
        GetTime = response.css('.post_time_source::text').extract()
        if GetTime:
            item['news_time'] = GetTime[0].strip().rstrip('　来源: ')

    def get_source(self, response, item):
        source = response.css('div.post_time_source a::text').extract() ## css查询时候的id用#表示
        if source:
            item['news_source'] = source[0]
        else:
            print(source)

    def get_source_url(self, response, item):
        source_url = response.css('div.post_time_source a::attr(href)').extract()
        if source_url:
            item['source_url'] = source_url[0]
        else:
            print(source_url[0])

    def get_text(self, response, item):
        text = response.css('.post_text p::text').extract()
        
        def change_text(text):
            for index, value in enumerate(text):
                text[index] = value.strip()
            return text

        if text:
            item['news_body'] = change_text(text)
        else:
            print(text) 
        
    def write_to_txt(self, item):
        with open('news163_data.txt', 'ab') as f:
            ## 每次只取最后一个
            f.seek(0)
            f.write('News Thread: {}'.format(item['news_thread']).encode())
            f.write('\r\n'.encode())
            f.write('News Title: {}'.format(item['news_title']).encode())
            f.write('\r\n'.encode())
            f.write('News Time: {}'.format(item['news_time']).encode())
            f.write('\r\n'.encode())
            f.write('News Source: {}'.format(item['news_source']).encode())
            f.write('\r\n'.encode())
            f.write('News URL: {}'.format(item['source_url']).encode())
            f.write('\r\n'.encode())
            f.write('News Body: {}'.format(item['news_body']).encode())
            f.write('\r\n'.encode())
            f.write(('_'*20).encode())
            f.write('\r\n'.encode())