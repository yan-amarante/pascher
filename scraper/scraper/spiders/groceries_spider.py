from pathlib import Path

import scrapy

class GroceriesSpider(scrapy.Spider):
    name = "groceries"

    def start_requests(self):
        urls = ["https://www.bistek.com.br/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"groceries-page{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")