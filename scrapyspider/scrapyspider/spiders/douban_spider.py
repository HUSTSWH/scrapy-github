# -*- coding:utf-8 -*-
#!/usr/bin/env python3

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import DoubanMovieItem

class DoubanMovieTop250Spider(Spider):
    name = 'douban_movie_top250'
    start_urls = [
        'https://movie.douban.com/top250',
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    def start_requests(self):
        for url in self.start_urls:
# yield Request(url, headers=self.headers)
            yield Request(url)

    def parse(self, response):
        item = DoubanMovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath(
                    './/div[@class="pic"]/em/text()'
                    ).extract_first()
            item['movie_name'] = movie.xpath(
                    './/div[@class="hd"]/a/span[1]/text()'
                    ).extract_first()
            item['score'] = movie.xpath(
                    './/div[@class="star"]/span[@class="rating_num"]/text()'
                    ).extract_first()
# item['score_num'] = movie.xpath(
# './/div[@class="star"]/span/text()'
# ).re(ur'(\d+)人评价')[0]
            yield item

