# -*- coding:utf-8 -*-
#!/usr/bin/env python3

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import GithubUserItem

class GithubUserSpider(Spider):
    name = 'github_user'
    header = 'https://github.com/'
    
    def start_requests(self):
        url = self.header + "HUSTSWH"
        yield Request(url, callback=self.parse_overview)

    def parse_overview(self, response):
        card = response.xpath('//div[@itemtype="http://schema.org/Person"]')
        item = GithubUserItem()
        item['username'] = card.xpath('//span[@itemprop="additionalName"]/text()').extract_first()
        item['name'] = card.xpath('//span[@itemprop="name"]/text()').extract_first()
        item['organization'] = card.xpath('//span[@class="p-org"]/div/text()').extract_first()
        item['url'] = card.xpath('//a[@class="u-url"]/text()').extract_first()

        url = self.header + item['username'] + '?tab=repositories'
        request =  Request(url, callback=self.parse_repo, priority=100)
        request.meta['item'] = item
        yield request

    def parse_repo(self, response):
        item = response.meta['item']
        repos = [s.strip() for s in response.xpath('//a[@itemprop="name codeRepository"]/text()').extract()]
        item['repos'] = str(repos)

        url = self.header + item['username'] + '?tab=followers'
        request = Request(url, callback=self.parse_followers, priority=200)
        request.meta['item'] = item
        yield request

    def parse_followers(self, response):
        item = response.meta['item']
        users = [s[1:] for s in response.xpath('//a[@class="d-inline-block no-underline mb-1"]/@href').extract()]
        item['followers'] = str(users)

        url = self.header + item['username'] + '?tab=following'
        request = Request(url, callback=self.parse_following, priority=300)
        request.meta['item'] = item
        yield request

        for next_user in users:
            url = self.header + next_user
            yield Request(url, callback=self.parse_overview)

    def parse_following(self, response):
        item = response.meta['item']
        users = [s[1:] for s in response.xpath('//a[@class="d-inline-block no-underline mb-1"]/@href').extract()]
        item['following'] = str(users)

        yield item

        for next_user in users:
            url = self.header + next_user
            yield Request(url, callback=self.parse_overview)

