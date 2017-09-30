# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LineblogscraperItem(scrapy.Item):

    author = scrapy.Field()
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    article_datetime = scrapy.Field()
    article_body = scrapy.Field()
    article_tag = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
