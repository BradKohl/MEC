import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]"):
            yield {
                'text': quote.xpath('//*[contains(@class, "text")]/text()').get(),
                'author': quote.xpath('//*[contains(@class, "author")]/text()').get(),
                'tags': quote.xpath('//*[contains(@class, "tags")]/*/text()').getall(),
            }

        # SUPER SHORT FOLLOW LINK
        yield from response.follow_all(xpath='//*[contains(@class, "next")]/a', callback=self.parse)

        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
