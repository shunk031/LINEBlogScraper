# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from LINEBlogScraper.items import LineblogscraperItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LineblogscraperPipeline(object):

    def process_item(self, item, spider):
        return item


class ValidationPipeline(object):

    ITEM = LineblogscraperItem()

    def process_item(self, item, spider):

        for key in self.ITEM.fields.keys():

            if key == 'article_tag':
                continue

            if not item[key]:
                raise DropItem('Missing {}'.format(key.split(' ')))

        return item


class FormatArticleBody(object):

    def process_item(self, item, spider):
        item['article_body'] = self.remove_non_break_space(item['article_body'])
        item['article_body'] = self.remove_tab(item['article_body'])
        item['article_body'] = self.remove_space(item['article_body'])
        item['article_body'] = self.remove_newline_code(item['article_body'])

        return item

    def remove_non_break_space(self, sentence_list):
        return [s.replace('\xa0', '') for s in sentence_list]

    def remove_space(self, sentence_list):
        return [s.replace(' ', '') for s in sentence_list]

    def remove_tab(self, sentence_list):
        return [s.replace('\t', '') for s in sentence_list]

    def remove_newline_code(self, sentence_list):
        sentence_list = [s.replace('\n', '').replace('\r', '') for s in sentence_list]
        while sentence_list.count('') > 0:
            sentence_list.remove('')

        return sentence_list


class FormatArticleTitle(object):

    def process_item(self, item, spider):

        item['article_title'] = self.remove_newline_code(item['article_title'])
        item['article_title'] = self.remove_space(item['article_title'])

        return item

    def remove_newline_code(self, s):
        return s.replace('\n', '').replace('\r', '')

    def remove_space(self, s):
        return s.replace(' ', '')
