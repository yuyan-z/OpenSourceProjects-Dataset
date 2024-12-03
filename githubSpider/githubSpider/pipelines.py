# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GithubspiderPipeline:
    def __init__(self):
        self.file = open('items.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        self.file.write(json.dumps(item)+',\n')
        return item

    def close_spider(self, spider):
        self.file.close()