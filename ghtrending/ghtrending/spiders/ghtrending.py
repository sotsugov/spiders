# -*- coding: utf-8 -*-
import os
import scrapy


class GitHubTrendingSpider(scrapy.Spider):
    name = "ghtrending"
    languages = ['python', 'jupyter-notebook']

    def start_requests(self):
        url = 'https://github.com/trending/{}'
        for language in self.languages:
            yield scrapy.Request(url=url.format(language), callback=self.parse)

    def parse(self, response):
        for repo in response.css('ol.repo-list li'):
            try_desc = repo.css('p::text').extract_first()
            yield {
                'title': repo.css('a::attr(href)').extract_first(),
                'desc': try_desc.strip() if try_desc else 'No description',
                'authors': repo.css('img::attr(title)').extract()
            }

