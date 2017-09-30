# -*- coding: utf-8 -*-

import hashlib

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from scrapy.http import Request
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


class LineBlogImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'author': item['author']})
                for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        # start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        # end of deprecation warning block

        author = request.meta['author']

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return 'full/%s/%s.jpg' % (author, image_guid)
