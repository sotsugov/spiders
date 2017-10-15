# -*- coding: utf-8 -*-
import os
import scrapy


class RedditDailyTopSpider(scrapy.Spider):
    name = "rdailytop"
    subreddits = ['technology', 'dataisbeautiful', 'MachineLearning',
                  'python', 'programming']
    n_stories = 5

    def start_requests(self):
        url = 'https://www.reddit.com/r/{}/top/?sort=top&t=day'
        for subreddit in self.subreddits:
            yield scrapy.Request(url=url.format(subreddit), callback=self.parse)

    def parse(self, response):
        for thing in response.css('.thing')[:self.n_stories]:
            yield {
                "title": thing.css('.title::text').extract_first(),
                "href": thing.css('.title a::attr(href)').extract_first(),
                "comments":  thing.css('.first a::attr(href)').extract_first(),
            }

