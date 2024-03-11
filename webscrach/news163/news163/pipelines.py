# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pickle

# 在setting.py中取消ITEM_PIPELINES的注释：
class News163Pipeline:
    def __init__(self):
        self.file = open('_article.json', 'w')
        pass

    # 以item为单位处理 
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(content+'\n')
        return item
    
    def close_spider(self, spider):
        self.file.close()