# -*- coding: utf-8 -*-

import scrapy
from LINEBlogScraper.items import LineblogscraperItem


class LineblogScraperBaseSpider(scrapy.Spider):
    name = 'lineblog_base_scraper'
    allowed_domains = ['lineblog.me']
    start_urls = ['http://lineblog.me/']

    elements = {
        'article_url': 'article h1 a::attr("href")',
        'article_title': 'article h1.article-title a::text',
        'article_datetime': 'article p.article-date time::attr("datetime")',
        'article_body': 'article div.article-body ::text',
        'article_tag': 'article dl.article-tags dd ::text',
        'image_urls': 'article a img::attr("src")',
        'next_page': 'div.pager li.paging-next a::attr("href")',
    }

    def parse(self, response):

        urls = response.css(self.elements['article_url']).extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), self.parse_articles)

        next_page = response.css(self.elements['next_page']).extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)

    def parse_articles(self, response):

        item = LineblogscraperItem()
        item['article_url'] = response.url
        item['article_title'] = response.css(self.elements['article_title']).extract_first()
        item['article_datetime'] = response.css(self.elements['article_datetime']).extract_first()
        item['article_body'] = response.css(self.elements['article_body']).extract()
        item['article_tag'] = response.css(self.elements['article_tag']).extract()
        item['image_urls'] = response.css(self.elements['image_urls']).extract()

        yield item


class LineblogScraperSpider(LineblogScraperBaseSpider):
    name = 'lineblog_scraper'

    def __init__(self, *args, **kwargs):
        super(LineblogScraperSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
