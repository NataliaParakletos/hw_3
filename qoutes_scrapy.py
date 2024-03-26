import scrapy
import json
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'quotes.json'
})

process.crawl(QuotesSpider)
process.start()

# Save authors to a separate JSON file
with open('quotes.json') as f:
    quotes_data = json.load(f)

authors_data = {}
for quote in quotes_data:
    author = quote['author']
    if author not in authors_data:
        authors_data[author] = {
            'name': author,
            'quotes': []
        }
    authors_data[author]['quotes'].append(quote['text'])

with open('authors.json', 'w') as f:
    json.dump(list(authors_data.values()), f)
