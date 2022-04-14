import scrapy
import json
import re
from msrp_alpina.spiders.post_appraise import post_appraise


class AlpinaSpider(scrapy.Spider):
    name = 'alpina'

    def __init__(self, market, api="https://appraise.cosmos.ieplsg.com/v1/api"):
        self.sourceId = 0
        self.type = 'OFFICIAL'
        self.brand_id = 288
        self.result = []
        self.market = market.upper()
        self.api = api
        if self.market == 'USA':
            self.base = 'https://alpinawatches.com'
            self.urls = [
                'https://us.alpinawatches.com/collections/alpiner',
                'https://us.alpinawatches.com/collections/comtesse',
                'https://us.alpinawatches.com/collections/seastrong',
                'https://us.alpinawatches.com/collections/startimer',
                'https://us.alpinawatches.com/collections/new-arrivals',
                'https://us.alpinawatches.com/collections/smartwatch',
            ]
            self.currency_id = 2
            self.tax_rate = 0
            self.precision = 2
        # elif self.market == 'JPN':
        #     self.base = ''
        #     self.entry = ['']
        #     self.currency_id = 7
        #     self.tax_rate = 10
        #     self.precision = 0
        # elif self.market == 'DNK':
        #     self.base = 'https://alpinawatches.com'
        #     self.urls = [
        #         'https://alpinawatches.com/collections/alpiner',
        #         'https://alpinawatches.com/collections/startimer',
        #         'https://alpinawatches.com/collections/seastrong',
        #         'https://alpinawatches.com/collections/comtesse',
        #         'https://alpinawatches.com/collections/alpinerx',
        #         'https://alpinawatches.com/collections/startimerx',
        #         'https://alpinawatches.com/collections/horological-smartwatches',
        #         'https://alpinawatches.com/collections/alpinerx-alive',
        #         'https://alpinawatches.com/collections/alpinerx-smart-outdoors',
        #         'https://alpinawatches.com/collections/smartwatch-comtesse',
        #         'https://alpinawatches.com/collections/startimerx',
        #         'https://alpinawatches.com/collections/smartwatch',
        #     ]
        #     self.currency_id = 6
        #     self.tax_rate = 25
        #     self.precision = 0
        # elif self.market == 'TWN':
        #     self.base = ''
        #     self.entry = ['']
        #     self.currency_id = 10
        #     self.tax_rate = 5
        #     self.precision = 0
        # elif self.market == 'FRA':
        #     self.base = ''
        #     self.entry = ['']
        #     self.currency_id = 4
        #     self.tax_rate = 20
        #     self.precision = 0

    def start_requests(self):
        for url in self.urls:
            print('url : ', url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.market == 'DNK':
            ccode = 'ch'
            # No DNK market, official website using CHF
            #
            # for data in response.css('.bold-product-json::text'):
            #     jdata = json.loads(data.get())
            #     variants = jdata['variants']
            #     if variants:
            #         for variant in variants:
            #             if variant['title'] == ccode:
            #                 reference = variant['sku']
            #                 price = variant['price']
            #                 self.result.append(
            #                     {'reference': reference, 'amount': price / 100})
            # print({'reference': variant['sku'], 'amount': variant['price'] / 100})
        elif self.market == 'USA':
            ccode = 'us'
            for product in response.css('.ProductItem__Info'):
                reference = product.css(
                    'a::attr("href")').get().split("/").pop().upper()
                price = product.css('.ProductItem__Price::text').get()
                amount = float(re.sub(r"\D", "", price)) / 100
                self.result.append(
                    {'reference': reference, 'amount': amount})
                # print(reference, price, amount)

        next_page = response.css('link[rel="next"]::attr("href")').get()
        if next_page is not None:
            next_url = self.base + next_page
            print('url : ', next_url)
            yield response.follow(next_url, self.parse)
        else:
            post_appraise(self)
            # print(self.result)
