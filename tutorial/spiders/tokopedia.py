# -*- coding: utf-8 -*-
import scrapy


class TokopediaSpider(scrapy.Spider):
    name = 'tokopedia'
    allowed_domains = ['www.tokopedia.com']
    start_urls = ['https://www.tokopedia.com/p/handphone-tablet/handphone?page=3']

    def parse(self, response):
        for ad_url in response.css("#search-result div._2p2-wGqG > div._33JN2R1i > ._27sG_y4O a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(ad_url), callback=self.parse_ad_page)
        next_page = response.css("span._1Jiz_Hd8 span._2AsEdCKK > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_ad_page(self, response):
        item = {}
        product = response.css("#content-container")
        item["title"] = response.css('h1.rvm-product-title span::text').extract_first()
        item['category'] = response.css('.breadcrumb li[itemprop="itemListElement"] a span::text').extract()[1]
        item['description'] = ''.join(response.css('#info::text').extract())
        item['price'] = response.css('span[itemprop="price"]::text').extract_first()
        yield item
