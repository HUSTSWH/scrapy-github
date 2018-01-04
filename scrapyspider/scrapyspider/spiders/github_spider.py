# -*- coding:utf-8 -*-
#!/usr/bin/env python3

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import GithubUserItem

class GithubUserSpider(Spider):
    name = 'github_user'
    host = 'https://github.com/'
    
    def start_requests(self):
        url = self.host + "HUSTSWH"
        yield Request(url, callback=self.parse_overview)

    def parse_overview(self, response):
        card = response.xpath('//div[@itemtype="http://schema.org/Person"]')
        item = GithubUserItem()
        item['username'] = card.xpath('//span[@itemprop="additionalName"]/text()').extract_first()
        item['name'] = card.xpath('//span[@itemprop="name"]/text()').extract_first()
        item['organization'] = card.xpath('//span[@class="p-org"]/div/text()').extract_first()
        item['url'] = card.xpath('//a[@class="u-url"]/text()').extract_first()

        # convey current fields to next page
        url = self.host + item['username'] + '?tab=repositories'
        request =  Request(url, callback=self.parse_repo, priority=100)
        request.meta['item'] = item
        yield request

    def parse_repo(self, response):
        # get item with fields from previous page
        item = response.meta['item']
        repos = response.xpath('//a[@itemprop="name codeRepository"]/text()').extract()
        item['repos'] = [{"name": reponame.strip()} for reponame in repos]

        url = self.host + item['username'] + '?tab=followers'
        request = Request(url, callback=self.parse_followers, priority=200)
        request.meta['item'] = item
        yield request

    def parse_followers(self, response):
        item = response.meta['item']
        users = response.xpath('//a[@class="d-inline-block no-underline mb-1"]/@href').extract()
        # erase '/' in the front of name. '/HUSTSWH' -> 'HUSTSWH'
        users = [user[1:] for user in users]
        item['followers'] = [{"username": user} for user in users]

        url = self.host + item['username'] + '?tab=following'
        request = Request(url, callback=self.parse_following, priority=300)
        request.meta['item'] = item
        yield request

        # add homepage of followers to the query
        for next_user in users:
            url = self.host + next_user
            yield Request(url, callback=self.parse_overview)

    def parse_following(self, response):
        item = response.meta['item']
        users = response.xpath('//a[@class="d-inline-block no-underline mb-1"]/@href').extract()
        users = [user[1:] for user in users]
        item['following'] = [{"username": user} for user in users]
        
        # All fields crawled, return item to the engine.
        yield item

        # add homepage of following to the query
        for next_user in users:
            url = self.host + next_user
            yield Request(url, callback=self.parse_overview)

