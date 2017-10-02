# -*- coding: utf-8 -*-
import os
import scrapy
from datetime import datetime

class HackerNewsSpider(scrapy.Spider):
    name = "hnkw"
    stories = {}

    def start_requests(self):
        url = 'https://news.ycombinator.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for story in response.css('.storylink'):
            self.stories[story.css('a::text').extract_first()] = \
                story.css('a::attr(href)').extract_first()

        keywords = ['python', 'data', ' ai ', ' ml ',
                    'deep learning', 'machine learning', 'firefox',
                    'mozilla']
        SOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
        SOURCES_PATH = os.path.join(SOURCES_DIR, 'data/hnkw.txt')

        with open(SOURCES_PATH, 'a') as f:
            f.write("{}\n".format(datetime.utcnow()))
            for item, url in self.stories.items():
                for keyword in keywords:
                    if keyword in item.lower():
                        f.write("[{}] {}: {}\n".format(
                            keyword, item.encode('utf-8'), url))

        self.log('Saved file {}'.format(SOURCES_PATH))
