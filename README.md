# LINEBlogScraper

Scraper for [LINE BLOG](https://www.lineblog.me/) in Scrapy.

## Requirements

* Python 3.5.1
* Scrapy 1.4.0

## How to run

crawl https://lineblog.me//TARGET_BLOG and output blog.json

``` shell
scrapy crawl lineblog_scraper -a start_url='https://lineblog.me/TARGET_BLOG' -o blog.json
```

## Downloading images

Will be downloaded and stored in the following directory: `LINEBlogScraper/images/full/`
