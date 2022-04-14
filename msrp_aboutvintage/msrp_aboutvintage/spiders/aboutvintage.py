import scrapy
import re
from msrp_aboutvintage.spiders.post_appraise import post_appraise


class AboutvintageSpider(scrapy.Spider):
    name = 'aboutvintage'
    allowed_domains = ['aboutvintage.com']

    def __init__(self, market, api="https://appraise.cosmos.ieplsg.com/v1/api"):
        self.sourceId = 0
        self.type = 'OFFICIAL'
        self.brand_id = 152
        self.result = []
        self.market = market.upper()
        self.api = api
        if self.market == 'USA':
            self.base = 'https://aboutvintage.com'
            self.entry = 'https://aboutvintage.com/collections/all-watches'
            self.currency_id = 2
            self.tax_rate = 0
            self.precision = 2
        elif self.market == 'JPN':
            self.base = 'https://jp.aboutvintage.com'
            self.entry = "https://jp.aboutvintage.com/collections/all-watches"
            self.currency_id = 7
            self.tax_rate = 10
            self.precision = 0
        elif self.market == 'DNK':
            self.base = 'https://dk.aboutvintage.com'
            self.entry = 'https://dk.aboutvintage.com/collections/alle-ure'
            self.currency_id = 6
            self.tax_rate = 25
            self.precision = 0
        elif self.market == 'TWN':
            self.base = 'https://tw.aboutvintage.com'
            self.entry = 'https://tw.aboutvintage.com/collections/all-watches'
            self.currency_id = 10
            self.tax_rate = 5
            self.precision = 0
        elif self.market == 'FRA':
            self.base = 'https://fr.aboutvintage.com'
            self.entry = 'https://fr.aboutvintage.com/collections/all-watches'
            self.currency_id = 4
            self.tax_rate = 20
            self.precision = 0

    def start_requests(self):
        urls = [self.entry]
        for url in urls:
            print('url : ', url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for product in response.css('.ProductListWrapper .ProductItem__Wrapper'):
            reference = product.css(
                "a::attr('href')").get().split('/').pop().upper()
            price = product.css(
                'a .ProductItem__PriceList .ProductItem__Price::text').get()
            if price:
                amount = float(re.sub(r"\D", "", price))
            else:
                amount = 0
            self.result.append({"reference": reference, "amount": amount})

        next_page = response.css('.AjaxinatePagination a::attr("href")').get()
        if next_page is not None:
            next_url = self.base + next_page
            print('url : ', next_url)
            yield response.follow(next_url, self.parse)
        else:
            post_appraise(self)
