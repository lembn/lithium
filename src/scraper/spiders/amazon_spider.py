import re
from itertools import chain, product
import requests
from battery import Battery
from lxml.html import fromstring


class AmazonSpider:
    asins = []

    def __init__(self, domain):
        self.url = f"https://www.amazon.{domain}"

    def crawl(self, queries: list[str]):
        urls = (f"{self.url}s?k={'+'.join(query.split())}" for query in queries)
        yield chain(self.scrape(url, 1) for url in urls)

    def scrape(self, url: str, page: int):
        html = fromstring(requests.get(f"{url}&page={page}").text)
        products = html.xpath("//[@data-asin]")

        next_btn = html.xpath('//li[@class="a-disabled a-last"]')
        if len(next_btn) == 0:
            yield self.scrape(url, page + 1)

        yield (
            self.build_product(product["data-asin"])
            for product in products
            if product["data-asin"] not in self.asins
        )

    # TODO: scrape mass (probably regex search for 'weight: ng')
    # TODO: scrape price
    def build_product(self, asin: str) -> dict[str, Battery]:
        url = f"{self.url}/dp/{asin}"
        res = requests.get(url).text
        parsed_html = fromstring(res)
        about_list = parsed_html.xpath('//div[@id="feature-bullets"]/ul')
        yield {
            asin: Battery(
                asin,
                re.search("\d+(?=m(a|A)h)", about_list.text).group(),
                re.search("\d+(?=g)", about_list.text).group()[0],
                url,
                about_list.xpath('//span[@class="a-price"]/span').text(),
            )
        }
