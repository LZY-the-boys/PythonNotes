import scrapy
import json
import requests
import logging
import os
from datetime import datetime
import pickle
import signal

def prepare_dirs_loggers(log_dir, script=""):
    logFormatter = logging.Formatter("%(levelname)s|%(asctime)s|%(message)s") # %(pathname)s:%(lineno)s
    Logger = logging.getLogger()
    Logger.setLevel(logging.DEBUG)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    time_stamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    script = script
    dir_name = "{}-{}".format(time_stamp, script) if script else time_stamp
    session_dir = os.path.join(log_dir, dir_name)
    os.mkdir(session_dir)

    fileHandler = logging.FileHandler(os.path.join(session_dir,'session.log')) # 显然不会包含print的东西
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(logFormatter)
    Logger.addHandler(fileHandler)
    return Logger,session_dir

logger,session_dir = prepare_dirs_loggers('./log') # 运行目录...






class News163Spider(scrapy.Spider):
    name = 'news.163'
    # allowed_domains = ['news.163.com'] 坑了
    media_xhr_prefix = 'https://dy.163.com/v2/article/list.do?'
    # >网易号>正文
    article_prefix = 'https://www.163.com/dy/article/'

    need_same_media_articles = False
    need_recommend_articles = True
    
    def custom_terminate_spider(self, sig, frame):
        pickle.dump(self.urlset,open(f'{self.logdir}/urlset.pkl','wb'))
        #dangerous line, it will just kill your scrapy spider running immediately
        os.kill(os.getpid(), signal.SIGKILL)


    def start_requests(self):
        self.urlset = pickle.load(open('log/2022-05-29T11-34-42/urlset.pkl','rb'))
        self.logdir = session_dir
        signal.signal(signal.SIGINT, self.custom_terminate_spider) #CTRL+C
        signal.signal(signal.SIGTERM, self.custom_terminate_spider) #sent by scrapyd
        # 分类收集

        start_url = [
            'https://news.163.com',
            'https://gov.163.com/',
            'https://media.163.com/',
            'https://war.163.com/',
            'https://money.163.com/',
            'https://tech.163.com/',
            'https://sports.163.com/',
            'https://sh.house.163.com/', # 仅限上海
            'https://news.163.com/world/', # 国际新闻
            'https://news.163.com/domestic/', # 国内新闻
            'https://news.163.com/air/',#航空
            'https://ent.163.com/', # 娱乐
            'https://auto.163.com/', # 汽车
        ]
        parse_function =[
            self.main_page_parse,
            self.gov_page_parse,
            self.media_page_parse,
            self.war_page_parse,
            self.money_page_parse,
            self.tech_page_parse,
            self.sports_page_parse,
            self.house_page_parse,
            self.news_page_parse,
            self.news_page_parse,
            self.airnews_page_parse,
            self.ent_page_parse,
            self.car_page_parse,

        ]
        for topic in range(len(start_url)):
            yield scrapy.Request(url=start_url[topic], callback=parse_function[topic],dont_filter=True)

    def isduplicate(self,url):
        urlpart = url.split('/')[-1].split('.')[0]
        return urlpart in self.urlset

    def war_page_parse(self,response):
        # https://war.163.com/

        # 今日推荐(已经包含在信息流内)
        # for today_url in response.xpath("//div[@class='today_news']//li/a/@href").extract():
        war_urls = response.xpath("//div[@class='second_left']//div[@class='hidden']//a/@href").extract()
        if war_urls == []:
            logger.error('>>> war page extract nothing')   
           
        # 左侧信息流
        for url in war_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url:
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'war'},dont_filter=True)
            # bug: 军事的推荐也可能是不同类型的
        # 右侧信息流

    def money_page_parse(self,response):
        money_urls = response.xpath("//body/div[@id='index2016_wrap']/div/div[@class='index2016_content']/div[@class='idx_main idx_main3 common_wrap clearfix']/div[1]//a/@href").extract()
        if money_urls == []:
            logger.error('>>> money page extract nothing')

        for url in money_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url:
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'money'},dont_filter=True)


    def tech_page_parse(self,response):
        tech_urls = response.xpath("//body/div[@id='index2016_wrap']/div[@class='index2016_content']/div[@class='main-news-area clearfix']/div[1]//a/@href").extract()
        if tech_urls == []:
            logger.error('>>> sports page extract nothing')

        for url in tech_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url:
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'tech'},dont_filter=True)

    def sports_page_parse(self,response):
        tech_urls = response.xpath("//li[@class='newsdata_item']//a/@href").extract()
        if tech_urls == []:
            logger.error('>>> sports page extract nothing')

        for url in tech_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                # 诸如https://sports.163.com/19/1124/12/xxx.html这样的也可以，但这里直接忽略
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'sports'},dont_filter=True)    

    def house_page_parse(self,response):
        tech_urls = response.xpath("//div[@class='data_row news_article clearfix2 ']//a/@href").extract()
        if tech_urls == []:
            logger.error('>>> house page extract nothing')

        for url in tech_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'house'},dont_filter=True) 

    def news_page_parse(self,response):
        tech_urls = response.xpath("//div[@class='second_left']//div[@class='hidden']//a/@href").extract()
        if tech_urls == []:
            logger.error('>>> news page extract nothing')

        for url in tech_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'news'},dont_filter=True) 
    
    def airnews_page_parse(self,response):
        air_urls =  response.xpath("//div[@class='hidden']//a/@href").extract()
        if air_urls == []:
            logger.error('>>> airnews page extract nothing')

        for url in air_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'air'},dont_filter=True)      
  
    def ent_page_parse(self,response):
        tech_urls = response.xpath("//li[@class='newsdata_item']//div[@class='ndi_main']//a/@href").extract()
        if tech_urls == []:
            logger.error('>>> ent page extract nothing')

        for url in tech_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'ent'},dont_filter=True) 

    def car_page_parse(self,response):
        tech_urls = response.xpath("(//div[@id='s-carnews'])[1]//a/@href").extract()
        if tech_urls == []:
            logger.error('>>> car page extract nothing')

        for url in tech_urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'car'},dont_filter=True)   
    
    def gov_page_parse(self,response):

        _urls = requests.get('https://gov.163.com/special/00239AOT/index2022_datalist.js?callback=data_callback&_=1653793616885').content # unix time
        _urls = json.loads(_urls.decode('utf-8')[14:-1]) # 离谱
        _urls = [data['docurl'] for data in _urls]

        urls = response.xpath("//div[@class='hot_news']//a/@href").extract()
        urls.extend(_urls)

        for url in urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'gov'},dont_filter=True)          

    def media_page_parse(self,response):
        urls = response.xpath("//div[@class='list_message']//a/@href").extract()
        for url in urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,meta={'kind': 'media'},dont_filter=True)  

    def main_page_parse(self, response):
        # news.163.com
        # 在主页首先获取一批最新的url
        urls = response.xpath("//li[@class='newsdata_item']//a/@href").extract()
        
        # 根据这些url递归爬取
        for url in urls:
            if self.isduplicate(url):
                continue
            if 'article' in url: 
                yield scrapy.Request(url=url,callback=self.article_parse,dont_filter=True)  

    def article_parse(self,response):
        sen_symbol = [',','，','.','。','?','？','!','！']
        article_url = response.url
        # check
        urlpart = article_url.split('/')[-1].split('.')[0]
        if urlpart in self.urlset:
            logger.info(f'[duplicated]{article_url}')
            # 如果爬的话会死循环              
            return
        logger.info(f'[request]{article_url}')
        self.urlset.add(urlpart)

        try:
            title = response.xpath("//h1[@class='post_title']/text()").extract()[0]
        except IndexError: # 网易红彩
            return

        # 获取该媒体其它文章url
        # bug: same user 不断递归
        try:
            media_id = response.xpath("//div[@id='contain']/@data-wemediaid").extract()[0]
        except IndexError:
            media_id = -1 # 有的页面没有
        if self.need_same_media_articles:
            request_url = self.media_xhr_prefix + f'pageNo=0&wemediaId={media_id}&size=10'
            same_content = requests.get(request_url).content
            js_content = json.loads(same_content)
            same_urls = []
            for data in js_content['data']['list']:
                doc_id = data['docid']
                same_urls.append(self.article_prefix+doc_id+'.html')
                break 
            for url in same_urls: 
                yield scrapy.Request(url=url, callback=self.article_parse,dont_filter=True)

        content = ''
        for text in response.xpath("//div[@class='post_body']/p/text()").extract():
            text = text.strip() 
            if len(text) < 5 or all([s not in text for s in sen_symbol]):
                continue
            content += text

        time = response.xpath("//div[@class='post_info']/text()").extract()[0]
        time = time.strip()[:19]#' 来源'
        media_name = response.xpath("//div[@class='post_info']//a[1]/text()").extract()[0].strip()
        # 新闻主体内容解析完毕，生成数据
        yield {
            'time': time,
            # 'kind': response.meta.get('kind'), # 即使是军事点进去，推荐也可能是别的类别的
            'url': article_url,
            'title': title,
            'content': content,
            'media_name':media_name,
            'media_id':media_id
        } # -> call item pipeline

        # 获取推荐新闻
        if self.need_recommend_articles:
            recommend_url = response.xpath("//div[@class='post_recommends js-tab-mod']//a[@class='post_recommend_img']/@href").extract()
            for url in recommend_url:
                url = url[:url.find('?')] # '?f=post2020_dy_recommends'
                if 'video' in url:
                    continue
                if self.isduplicate(url):
                    continue
                yield scrapy.Request(url,callback=self.article_parse,dont_filter=True) 


    # 无法调函数...
    def get_recommend_articles(self,recommend_url):
        for rurl in recommend_url:
            rurl = rurl[:rurl.find('?')] # '?f=post2020_dy_recommends'
            if 'video' in rurl:
                continue
            if rurl in self.url_set:
                continue
            yield scrapy.Request(rurl,callback=self.article_parse,headers=self.header)

    def get_this_media_articles(self,media_id):
        # 获取该媒体其它文章
        # media_id = 'W2487216988678436106'
        request_url = self.media_xhr_prefix + f'pageNo=0&wemediaId={media_id}&size=10'
        
        response = requests.get(request_url).content
        jsonBody = json.loads(response)
        same_urls = []
        for data in jsonBody['data']['list']:
            import pdb;pdb.set_trace()
            doc_id = data['docid']
            same_urls.append(self.article_prefix+doc_id+'.html')
            
        for url in same_urls:
            yield scrapy.Request(url=url, callback=self.article_parse,headers=self.header)
        pass
