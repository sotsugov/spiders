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
        for item in response.css('.repo-list'):

            yield {
                "repo": item.css('li div h3 a::attr(href)').extract(),
                "title": item.css('li .py-1 p::text').extract(),
            }
