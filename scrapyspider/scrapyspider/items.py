# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DoubanMovieItem(scrapy.Item):
    ranking = scrapy.Field()
    movie_name = scrapy.Field()
    score = scrapy.Field()
    score_num = scrapy.Field()

class GithubUserItem(scrapy.Item):
    username = scrapy.Field()
    name = scrapy.Field()
    organization = scrapy.Field()
    url = scrapy.Field()
    repos = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()

