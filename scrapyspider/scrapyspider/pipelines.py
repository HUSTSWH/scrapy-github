# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class GithubUserPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client.test_database

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db.GithubUser.insert_one(dict(item))
        print("insert to GithubUser:", self.db.GithubUser.find_one({"name": item["name"]}))
        return item

